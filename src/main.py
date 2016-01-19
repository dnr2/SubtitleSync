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
import datetime

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
        # record start time to calculate total elapsed time.
        self.start_time = time.time()
        
        ####################################################
        # Converting from video to audio
        ####################################################        
        self.LogProgress(u'Extracting audio...')     
        v_m = video_manager(self.CHOSEN_VIDEO, self.gui_manager)
        self.AUDIO_FILE = v_m.get_audio_from_video()
        self.LogProgress(u'\nExtraction finished.\n')
        self.gui_manager.IncrimentGlobalProgressBar()
        
        ####################################################
        # Splitting audio file on silence
        ####################################################        
        self.LogProgress(u'\nDetecting speech segments...\n')
        s_d = silence_detector(self.gui_manager)
        self.MAP_INTERVALS = s_d.split_on_silence(self.AUDIO_FILE)       
        self.LogProgress(u'Found ' + str(len(self.MAP_INTERVALS)) + ' possible segments.')
        self.gui_manager.IncrimentGlobalProgressBar()
        
        ####################################################
        # Transcripting audio speech segments
        ####################################################        
        self.LogProgress(u'\nTranscripting speech segments...\n')
        self.s_r_m = speech_recognition_manager(self.gui_manager)
        self.TIMESTAMPED_TRANSCRIPTIONS = self.s_r_m.speech_to_text(self.MAP_INTERVALS)
        self.LogProgress(
            u'\n' + str(len(self.TIMESTAMPED_TRANSCRIPTIONS)) + 
            u' out of ' + str(len(self.MAP_INTERVALS)) + u' successful transcriptions.\n')
        for timestamped_text in self.TIMESTAMPED_TRANSCRIPTIONS:
            self.LogProgress(str(timestamped_text) + "\n")
        self.gui_manager.IncrimentGlobalProgressBar()        
        
    def RunMTPipeline(self):
        ####################################################
        # Reading subtitle file
        ####################################################
        self.LogProgress(u'\nReading subtitles...\n')
        self.strp = srt_parser()
        self.SUBTITLES = self.strp.parse_ms(self.CHOSEN_SRT)
        self.LogProgress(u'Read ' + str(len(self.SUBTITLES)) + u' subtitles.\n')
        self.gui_manager.IncrimentGlobalProgressBar()
        
        for timestamped_sub in self.SUBTITLES:
            self.LogProgress(unicode(timestamped_sub) + u"\n")
        
        ####################################################
        # Translating subtitles text
        ####################################################
        self.LogProgress(u'\nTranslating subtitles...')
        self.TRANSLATED_SUBTITLES = self.s_r_m.translate(
            copy.deepcopy(self.SUBTITLES), from_language = 'pt', to_language = 'en')
        self.LogProgress(
            u'\n' + str(len(self.TRANSLATED_SUBTITLES)) + u' out of ' + 
            str(len(self.SUBTITLES)) + u' successful translations.\n')
        for timestamped_sub in self.TRANSLATED_SUBTITLES:
            self.LogProgress(unicode(timestamped_sub) + u"\n")        
        self.gui_manager.IncrimentGlobalProgressBar()
        
    def RunSentenceAlignment(self):
        ####################################################
        # Matching subtitles with speech segments transcriptions
        ####################################################
        self.LogProgress(u'\nMatching subtitles and transcriptions...\n')
        m_m = matching_manager(self.gui_manager)
        self.CORRECTED_TIME_SUBTITLES = m_m.match_subs_trans(
            self.TRANSLATED_SUBTITLES, self.TIMESTAMPED_TRANSCRIPTIONS, self.SUBTITLES)        
        self.gui_manager.IncrimentGlobalProgressBar()
        
    def RunSubtitleSerializer(self):
        ####################################################
        # Writing results
        ####################################################        
        self.LogProgress(u'\nFinal subtitles...\n')
        for timestamped_sub in self.CORRECTED_TIME_SUBTITLES:
            self.LogProgress(str(timestamped_sub) + u"\n")
        
        self.LogProgress(u'\nWriting synchronized subtile in file...\n')
        # get original subtitle text
        subtitle_output_path = '%s-SYNC-%s.srt'%(self.CHOSEN_SRT[:-4], str(self.current_milli_time()))
        logs_output_path = os.path.join(os.getcwd(), "logs", "log-%s.txt"%(str(self.current_milli_time())))
        self.LogProgress(u'\nSaving subtitle in: ' + subtitle_output_path)
        open(subtitle_output_path, 'wb').write(self.strp.format_ms(self.CORRECTED_TIME_SUBTITLES))
        #calculate elapsed time.
        self.elapsed_time = int(time.time() - self.start_time)
        self.LogProgress(u'\nTime elapsed (hh:mm:ss): %s\n'%(str(datetime.timedelta(seconds=self.elapsed_time))))
        self.LogProgress(u'\n\nEnd of synchronization...')        
        # save logs in file.
        open(logs_output_path, 'wb').write(str(time.ctime()) + u"\n" + self.gui_manager.log_file_text)
        time.sleep(1)
        self.gui_manager.IncrimentGlobalProgressBar()
        time.sleep(1)

def main():
    MainClass().RunMain()
        
if __name__=='__main__':
    main()