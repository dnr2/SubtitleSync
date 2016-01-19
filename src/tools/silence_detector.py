import os
import subprocess
import re
import srt_parser as srtp

class silence_detector():
    
    def __init__(self, gui_manager):
        self.gui_manager = gui_manager
    
    def LogProgress(self, msg):
        self.gui_manager.LogProgress(msg)
    
    def detect_silence(self, audio_filename, noise_tolerance = 0.12, silence_duration = 0.45, max_duration = None, delta = 0.35):
        '''
            Detects periods of silence in the audio file.

            Args:
                audio_filename(string) full path of the wave file.
                noise_tolerance(double, optional) Set noise tolerance specified in amplitude ratio. Default is 0.12.
                silence_duration(double, optional) Set silence duration until notification (default is 0.5 seconds).
                max_duration(double, optional) output audio duration in seconds cannot be longer than this value

            Returns:
                list with time intervals with that correspond to noise (no silence) in the audio
        '''
        if audio_filename == None or audio_filename == '' or not audio_filename.endswith('.wav'):
            raise Exception('Invalid file.')

        convert_command = "ffmpeg -i {0} -af silencedetect=n={1}:d={2} -f null -"
        convert_command = convert_command.format(audio_filename, noise_tolerance, silence_duration)
        process = output = error = None

        try:
            process = subprocess.Popen(convert_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            output, error = process.communicate()
        except Exception, e:
            self.LogProgress(u'Exception when converting file. Reason: ' + unicode(e.message))

        if process != None:
            process.terminate()

        #It seems ffmpeg is directing the output to stderr instead of stdout...
        if error is None:
            return []
        else:
            tokens = filter( lambda a : len(a)>0, re.compile("[ \r\n,]").split(error))

            start_audio = [0.0]
            end_audio = []
            total_time = 0

            for idx in range(0,len(tokens)) :
                if tokens[idx] == "silence_start:" :
                    end_audio.append(float(tokens[idx+1]) + delta)
                if tokens[idx] == "silence_end:" :
                    start_audio.append(float(tokens[idx+1]) - delta )
                if tokens[idx] == "Duration:" :
                    total_time = float(tokens[idx+1].split(":")[2]) + delta

            end_audio.append(total_time)

            #if max_duration is not None and duration > max_duration:
                #TODO: has to cut more
            
            inter = filter(lambda a: a[0] + 1e-2 < a[1], zip(start_audio, end_audio))
            
            #merge intervals that are closer than 2 s and don't exceed 5 s duration
            sz = len(inter)
            if sz > 1:
                for i in reversed(range(sz-1)):
                    if inter[i+1][0] - inter[i][1] < 2.0 and inter[i+1][1] - inter[i][0] < 5.0:
                        inter[i] = (inter[i][0], inter[i+1][1])
                        del inter[i+1]
            return inter
                

    def split_on_silence(self, audio_filename, output_filename = None):
        '''
            Create new audio files by removing silences from the original audio file.

            Args:
                audio_filename(string) full path of the wave file.
                output_filename(string, optional) The prefix name for the output file (should not have extension '.wav').

            Returns:
                folder with trimmed files
        '''

        if audio_filename == None or audio_filename == '' or not audio_filename.endswith('.wav'):
            raise Exception('Invalid file.')

        if output_filename is None:
            output_filename = os.path.basename(audio_filename).split('.')[0]

        if not os.path.isdir(os.path.join('audio_samples', 'trimmed')):
            os.makedirs(os.path.join('audio_samples', 'trimmed'))

        if not os.path.isdir(os.path.join('audio_samples', 'trimmed', output_filename)):
            os.makedirs(os.path.join('audio_samples', 'trimmed', output_filename))

        intervals = self.detect_silence(audio_filename)
        map = []
        
        for idx in range(0,len(intervals)):
            start = intervals[idx][0]
            end = intervals[idx][1]
            duration = end - start

            output_path = os.path.join('audio_samples', 'trimmed', output_filename, output_filename)
            trim_command = "sox {0} {1}_{2}.wav trim {3} {4}"
            trim_command = trim_command.format(audio_filename, output_path, idx+1, start, duration)

            try:
                process = subprocess.Popen(trim_command, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                output, error = process.communicate()                
                map.append((self.to_ms(start), self.to_ms(end), '{0}_{1}.wav'.format(output_path, idx+1)))
            except Exception, e:
                self.LogProgress('Exception when triming file. Reason: ' + unicode(e.message))

        return map
    
    def to_ms(self, second ):
        return int(round(second * 1000))