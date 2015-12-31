import os
import sys
import copy
import functools
import threading
import time
from tools.video_manager import video_manager
from tools.srt_parser import srt_parser
from tools.silence_detector import silence_detector
from tools.speech_recognition_manager import speech_recognition_manager
from tools.matching_manager import matching_manager
from gui import GuiManager

class MainClass():
    
    def current_milli_time(self):
        return int(round(time.time() * 1000))
    
    def SyncBtnCallBack(self):
        self.CHOSEN_VIDEO = self.gui_manager.video_file_dialog.entry.get()
        self.CHOSEN_SRT = self.gui_manager.subtitle_file_dialog.entry.get()
        if (not self.CHOSEN_VIDEO.endswith('.mp4')) and (not self.CHOSEN_VIDEO.endswith('.avi')):
            self.gui_manager.DisplayPromptMsg('Error', 'Invalid video file extension.\nOnly .avi and .mp4 accepted.')
        elif not self.CHOSEN_SRT.endswith('.srt'):
            self.gui_manager.DisplayPromptMsg('Error', 'Invalid subtitle file extension.\nOnly .srt accepted.')
        else:
            self.gui_manager.InitSynchronizingProgressFrame()            
            self.worker_thread = threading.Thread(target=self.ExecuteSynchronization)
            self.worker_thread.start()
            # The next line will block while synchronization is not complete.
            self.gui_manager.UpdateSynchronizingProgressFrame()
            
    def ExecuteSynchronization(self):
        self.RunASRPipeline()
        self.RunMTPipeline()
        self.RunSentenceAlignment()
        self.RunSubtitleSerializer()
    
    def RunMain(self):
        ####################################################
        # Choose video and subtitle
        ####################################################
        SyncBtnCallBackPartial = functools.partial(MainClass.SyncBtnCallBack, self)
        self.gui_manager = GuiManager(SyncBtnCallBackPartial)       
        self.gui_manager.RunSubSyncGuiMainLoop()    
    
    def LogProgress(self, msg):
        self.gui_manager.LogProgress(msg)
    
    def RunASRPipeline(self):
        ####################################################
        # Converting from video to audio
        ####################################################        
        self.LogProgress('Extracting audio...')        
        v_m = video_manager(self.CHOSEN_VIDEO, self.gui_manager)
        self.AUDIO_FILE = v_m.get_audio_from_video()    
        self.LogProgress('\nExtraction finished.\n')
        
        ####################################################
        # Splitting audio file on silence
        ####################################################        
        self.LogProgress('\nDetecting speech segments...\n')
        s_d = silence_detector(self.gui_manager)
        self.MAP_INTERVALS = s_d.split_on_silence(self.AUDIO_FILE)       
        self.LogProgress('Found ' + str(len(self.MAP_INTERVALS)) + ' possible segments.')
        
        ####################################################
        # Transcripting audio speech segments
        ####################################################
        self.LogProgress('\nTranscripting speech segments...\n')
        self.s_r_m = speech_recognition_manager(self.gui_manager)
        self.TIMESTAMPED_TRANSCRIPTIONS = self.s_r_m.speech_to_text(self.MAP_INTERVALS)
        self.LogProgress(
            '\n' + str(len(self.TIMESTAMPED_TRANSCRIPTIONS)) + 
            ' out of ' + str(len(self.MAP_INTERVALS)) + ' successful transcriptions.\n')
        for timestamped_text in self.TIMESTAMPED_TRANSCRIPTIONS:
            self.LogProgress(str(timestamped_text) + "\n")
        
    def RunMTPipeline(self):
        ####################################################
        # Reading subtitle file
        ####################################################
        self.LogProgress('\nReading subtitles...\n')
        self.strp = srt_parser()
        self.SUBTITLES = self.strp.parse_ms(self.CHOSEN_SRT)
        self.LogProgress('Read ' + str(len(self.SUBTITLES)) + ' subtitles.\n')
        
        for timestamped_sub in self.SUBTITLES:
            self.LogProgress(unicode(timestamped_sub) + u"\n")
        
        ####################################################
        # Translating subtitles text
        ####################################################
        self.LogProgress('\nTranslating subtitles...')
        self.TRANSLATED_SUBTITLES = self.s_r_m.translate(
            copy.deepcopy(self.SUBTITLES), from_language = 'pt', to_language = 'en')
        self.LogProgress(
            '\n' + str(len(self.TRANSLATED_SUBTITLES)) + ' out of ' + 
            str(len(self.SUBTITLES)) + ' successful translations.\n')
        for timestamped_sub in self.TRANSLATED_SUBTITLES:
            self.LogProgress(unicode(timestamped_sub) + u"\n")        
        
        
    def RunSentenceAlignment(self):
        ####################################################
        # Matching subtitles with speech segments transcriptions
        ####################################################
        self.LogProgress('\nMatching subtitles and transcriptions...\n')
        m_m = matching_manager(self.gui_manager)
        self.CORRECTED_TIME_SUBTITLES = m_m.match_subs_trans(
            self.TRANSLATED_SUBTITLES, self.TIMESTAMPED_TRANSCRIPTIONS, self.SUBTITLES)        
        
    def RunSubtitleSerializer(self):
        ####################################################
        # Writing results
        ####################################################        
        self.LogProgress('\nFinal subtitles...\n')
        for timestamped_sub in self.CORRECTED_TIME_SUBTITLES:
            self.LogProgress(unicode(timestamped_sub) + u"\n")
            
        self.LogProgress('\nWriting synchronized subtile in file...\n')
        # get original subtitle text
        output_path = '%s-SYNC-%s.srt'%(self.CHOSEN_SRT[:-4], str(self.current_milli_time()))
        self.LogProgress('\nSaving subtitle in: ' + output_path)
        open(output_path, 'wb').write(self.strp.format_ms(self.CORRECTED_TIME_SUBTITLES))
        self.LogProgress('\n\nEnd of synchronization...')
        
        # TODO concurrency here
        self.gui_manager.progress_value = self.gui_manager.max_progress_value

def main():
    MainClass().RunMain()
        
if __name__=='__main__':
    main()