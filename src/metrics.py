import os
from tools.srt_parser import srt_parser
import random
import pprint as pp
import math
import numpy as np
import matplotlib.pyplot as plt

def gen_precision_recall_bar_graph(test_sets):
    i, j = (0,0)
    for movie in test_sets:
        test_set = test_sets[movie]
        N = 4
        PRECISION_Means = []
        RECALL_Means = []
        PRECISION_Devs = []
        RECALL_Devs = []
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        xticklabels = ('SyncMySub\nALL', 'AnchorPoints\nLINEAR', 'AnchorPoints\nCROP', 'AnchorPoints\nRAND')
        opacity = 0.8
        error_config = {'ecolor': '0.3'}
        
        for test_name in ["OUTPUT", "LINEAR", "CROP", "RAND"]: 
            test_data = test_set[test_name]            
            PRECISION_Means.append(test_data["PRECISION"])
            RECALL_Means.append(test_data["RECALL"])
            PRECISION_Devs.append(test_data["PRECISION_dev"])
            RECALL_Devs.append(test_data["RECALL_dev"])
        
        #fig, ax = plt.subplots()
        ax = plt.subplot2grid((3,2),(i, j))
        rects1 = ax.bar(ind, tuple(PRECISION_Means), width, color='b', \
                        alpha=opacity, yerr=PRECISION_Devs, error_kw=error_config)
        rects2 = ax.bar(ind + width, tuple(RECALL_Means), width, color='r', \
                        alpha=opacity, yerr=RECALL_Devs, error_kw=error_config)

        # add some text for labels, title and axes ticks        
        #ax.set_ylabel('Scores')
        
        #ax.set_title('Scores by set and method on clip: "' + movie + '"')
        ax.set_title(movie)
        ax.set_xticks(ind + width)
        ax.set_xticklabels(xticklabels)

        ax.legend((rects1[0], rects2[0]), ('PRECISION', 'RECALL'), bbox_to_anchor=(1.1, 1.3))


        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%.2f' % float(height),
                        ha='center', va='bottom')
        
        x1,x2,y1,y2 = plt.axis()
        plt.axis((x1,x2,y1,1.55))
        
        autolabel(rects1)
        autolabel(rects2)
        
        j += 1
        if j > 1:
            i += 1
            j = 0
        
    #plt.tight_layout()
    #print 'Saving file: plots\\%s.png'% movie.replace(" ", "_")
    #plt.savefig('plots\\%s.png'% movie.replace(" ", "_"))
    print 'Saving file: plots\\precision_recall.png'
    #plt.savefig('plots\\precision_recall.png')
    plt.show()


def gen_dist_bar_graph(test_sets):
    i, j = (0,0)
    for movie in test_sets:
        test_set = test_sets[movie]
        N = 4
        START_Means, END_Means, MID_Means = ([],[],[])
        
        DIST_START_dev, DIST_END_dev, DIST_MID_dev = ([],[],[])
        ind = np.arange(N)  # the x locations for the groups
        width = 0.28      # the width of the bars
        xticklabels = ('SyncMySub\nALL', 'AnchorPoints\nLINEAR', 'AnchorPoints\nCROP', 'AnchorPoints\nRAND')
        opacity = 0.8
        error_config = {'ecolor': '0.3'}
        
        for test_name in ["OUTPUT", "LINEAR", "CROP", "RAND"]: 
            test_data = test_set[test_name]            
            START_Means.append(test_data["DIST_START"])
            END_Means.append(test_data["DIST_END"])
            MID_Means.append(test_data["DIST_MID"])
            '''
            if test_name == "CROP":
                DIST_START_dev.append(0)
                DIST_END_dev.append(0)
                DIST_MID_dev.append(0)
            else:
            '''
            DIST_START_dev.append(test_data["DIST_START_dev"])
            DIST_END_dev.append(test_data["DIST_END_dev"])
            DIST_MID_dev.append(test_data["DIST_MID_dev"])
        
        #fig, ax = plt.subplots()
        ax = plt.subplot2grid((3,2),(i, j))
        rects1 = ax.bar(ind, tuple(START_Means), width, color='b', \
                        alpha=opacity, yerr=DIST_START_dev, error_kw=error_config)
        rects2 = ax.bar(ind + width, tuple(END_Means), width, color='r', \
                        alpha=opacity, yerr=DIST_END_dev, error_kw=error_config)
        rects3 = ax.bar(ind + 2*width, tuple(MID_Means), width, color='g', \
                        alpha=opacity, yerr=DIST_MID_dev, error_kw=error_config)

        # add some text for labels, title and axes ticks        
        ax.set_ylabel('Seconds')
        
        #ax.set_title('Scores by set and method on clip: "' + movie + '"')
        ax.set_title(movie)
        ax.set_xticks(ind + 1.5* width)
        ax.set_xticklabels(xticklabels)

        ax.legend((rects1[0], rects2[0], rects3[0]), ('DSTART', 'DEND', 'DMID'))


        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                        '%.1f' % float(height),
                        ha='center', va='bottom')
        
        x1,x2,y1,y2 = plt.axis()
        y2 = max(max(START_Means), max(END_Means), max(MID_Means))
        plt.axis((x1,x2,y1, 1.2 * y2))
        
        autolabel(rects1)
        autolabel(rects2)
        autolabel(rects3)
        
        j += 1
        if j > 1:
            i += 1
            j = 0
        
    #plt.tight_layout()
    #print 'Saving file: plots\\%s.png'% movie.replace(" ", "_")
    #plt.savefig('plots\\%s.png'% movie.replace(" ", "_"))
    #plt.savefig('plots\\dist.png')
    print 'Saving file: plots\\precision_recall.png'
    plt.show()

def get_sync_filename(ground_sub_file_name, test_name):
    return '%s-%s-SYNC.srt'%(ground_sub_file_name[:-4], test_name)   

# strp = str parser
def generate_LINEAR(ground_segments, sub_file_name, strp):
    linear_segnments = []
    for seg in ground_segments:
        start = 2 * seg[0] + 2000
        end = start + (seg[1] - seg[0])
        linear_segnments.append( (start, end, seg[2]) ) 
    subtitle_output_path = '%s-LINEAR.srt'%(sub_file_name[:-4])
    open(subtitle_output_path, 'wb').write(strp.format_ms(linear_segnments))
    return subtitle_output_path

# strp = str parser
def generate_CROP(ground_segments, sub_file_name, strp):
    linear_segnments = []
    for seg in ground_segments:
        start = seg[0]
        end = seg[1]
        # if greater than 20 seconds, adds more 40 seconds
        if seg[0] > 20000:
            start += 40000
            end += 40000
        linear_segnments.append( (start, end, seg[2])) 
    subtitle_output_path = '%s-CROP.srt'%(sub_file_name[:-4])
    open(subtitle_output_path, 'wb').write(strp.format_ms(linear_segnments))
    return subtitle_output_path

def generate_RAND(ground_segments, sub_file_name, strp):
    linear_segnments = []
    max_jump = 2000 # 2 seconds
    random.seed(3021937)
    sum_offset = int(random.random() * max_jump)
    for seg in ground_segments:
        # if greater than 20 seconds
        start = seg[0] + sum_offset
        end = seg[1] + sum_offset
        linear_segnments.append((start, end, seg[2]))
        sum_offset += int(random.random() * max_jump)
    subtitle_output_path = '%s-RAND.srt'%(sub_file_name[:-4])
    open(subtitle_output_path, 'wb').write(strp.format_ms(linear_segnments))
    return subtitle_output_path

##################################################################

#TODO this might not work in repeated subtitle texts
def get_matching(ground_segments, output_segments):
    matching = []
    ground_idx = 0
    for segment in output_segments:
        partial_matching = []
        # test if ground text is contained in output segment text
        while ground_idx < len(ground_segments) and ground_segments[ground_idx][2] in segment[2]:
            partial_matching.append(ground_idx)
            ground_idx += 1
        matching.append(partial_matching)
        
    assert ground_idx == len(ground_segments)
    return matching

def standard_deviation(vals, mean):
    delta = 0.0
    for v in vals:
        delta += (mean-v) * (mean-v)
    return math.sqrt(delta / len(vals))
    
def get_confusion_matrix(matching, ground_segments, output_segments):
    TP, ground_time_sum, output_time_sum = (0, 0, 0)
    
    #used to calculate the standard deviation
    PRECISION_vals, RECALL_vals = ([],[])
    
    for idx_output in range(len(output_segments)):       
        
        alpha = float(output_segments[idx_output][0])
        alpha_prime = float(output_segments[idx_output][1])
        
        #used to calculate the standard deviation
        TP_val, gts_val = (0,0)
        
        for idx_ground in matching[idx_output]:
            g = float(ground_segments[idx_ground][0])
            g_prime = float(ground_segments[idx_ground][1])
            
            TP_val += max(0.0, min(alpha_prime, g_prime) - max( alpha, g))
            gts_val += g_prime - g
        
        FP_val = gts_val - TP_val
        FN_val = (alpha_prime - alpha) - TP_val
        PRECISION_vals.append(TP_val / (TP_val + FP_val))
        RECALL_vals.append(TP_val / (TP_val + FN_val))
        
        ground_time_sum += gts_val
        TP +=  TP_val        
        output_time_sum += alpha_prime - alpha
    
    (TP, FP, FN) = (TP, ground_time_sum - TP, output_time_sum - TP)
    PRECISION = TP / (TP + FP)
    RECALL = TP / (TP + FN)
    
    PRECISION_dev = standard_deviation(PRECISION_vals, PRECISION)
    RECALL_dev = standard_deviation(RECALL_vals, RECALL)
    
    return (PRECISION, RECALL, PRECISION_dev, RECALL_dev)

def get_dists(matching, ground_segments, output_segments):
    DIST_START, DIST_END, DIST_MID = (0,0,0)
    DIST_START_vals, DIST_END_vals, DIST_MID_vals = ([],[],[])
    
    delta = len(output_segments)
    for idx_output in range(delta):       
        alpha = float(output_segments[idx_output][0])
        alpha_prime = float(output_segments[idx_output][1])        
        g = float(ground_segments[matching[idx_output][0]][0])
        g_prime = float(ground_segments[matching[idx_output][-1]][1])
        
        DIST_START_vals.append(abs(alpha - g) / 1000.0)
        DIST_END_vals.append(abs(alpha_prime - g_prime) / 1000.0)
        DIST_MID_vals.append(abs((alpha + (alpha_prime - alpha)/2.0) - (g + (g_prime - g)/2.0)) / 1000.0)
        
        DIST_START += abs(alpha - g)
        DIST_END += abs(alpha_prime - g_prime)
        DIST_MID += abs((alpha + (alpha_prime - alpha)/2.0) - (g + (g_prime - g)/2.0))
                
    # transform from milliseconds to seconds
    delta = float(delta) * 1000
    DIST_START /= delta
    DIST_END /= delta
    DIST_MID /= delta
    
    DIST_START_dev = standard_deviation(DIST_START_vals, DIST_START)
    DIST_END_dev = standard_deviation(DIST_END_vals, DIST_END)
    DIST_MID_dev = standard_deviation(DIST_MID_vals, DIST_MID)
    
    return (DIST_START, DIST_END, DIST_MID, DIST_START_dev, DIST_END_dev, DIST_MID_dev)



    
def main():    
    test_sets = {
        "Forrest Gump": {
            "GROUND" : { 
                "FILE" : "Forrest Gump (1-9) Movie CLIP - Peas and Carrots (1994) HD.srt" 
            },
            "OUTPUT" : {
                "FILE": "Forrest Gump (1-9) Movie CLIP - Peas and Carrots (1994) HD-SYNC-1452373563988.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {}
        },
        "Inception": {
            "GROUND" : { 
                "FILE" : "Inception #1 Movie CLIP - The Most Skilled Extractor (2010) HD.srt"
            },
            "OUTPUT" : {
                "FILE": "Inception #1 Movie CLIP - The Most Skilled Extractor (2010) HD-SYNC-1452125706245.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {} 
        },
        "Pulp Fiction": {
            "GROUND" : { 
                "FILE" : "Pumpkin and Honey Bunny - Pulp Fiction (1-12) Movie CLIP (1994) HD.srt"
            },
            "OUTPUT" : {
                "FILE": "Pumpkin and Honey Bunny - Pulp Fiction (1-12) Movie CLIP (1994) HD-SYNC-1452404625214.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {}
        },
        "The Dark Knight": {
            "GROUND" : { 
                "FILE" : "The Dark Knight (1-9) Movie CLIP - Kill the Batman (2008) HD.srt"
            },
            "OUTPUT" : {
                "FILE": "The Dark Knight (1-9) Movie CLIP - Kill the Batman (2008) HD-SYNC-1452052735377.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {}
        },
        "12 Angry Men": {
            "GROUND" : { 
                "FILE" : "12 Angry Men (1-10) Movie CLIP - Kids These Days (1957) HD.srt"
            },
            "OUTPUT" : {
                "FILE": "12 Angry Men (1-10) Movie CLIP - Kids These Days (1957) HD-SYNC-1452922788945.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {}
        },
        "The Matrix": {
            "GROUND" : { 
                "FILE" : "The Matrix (1-9) Movie CLIP - Living Two Lives (1999) HD.srt"
            },
            "OUTPUT" : {
                "FILE": "The Matrix (1-9) Movie CLIP - Living Two Lives (1999) HD-SYNC-1452917712227.srt"
            }, 
            "LINEAR" : {}, "CROP" : {}, "RAND" : {}
        }
    }
    
    GENERETE_FILES = False   
    strp = srt_parser()
    
    for movie in test_sets:
        print "#######################"
        print "#### running test for :", movie, "\n"
        test_set = test_sets[movie] 
        ground_filename = os.path.join(os.getcwd(), 'tests', test_set["GROUND"]["FILE"])
        
        if GENERETE_FILES:
            ground_segments = strp.parse_ms(ground_filename)
            print generate_LINEAR(ground_segments, ground_filename, strp)
            print generate_CROP(ground_segments, ground_filename, strp)
            print generate_RAND(ground_segments, ground_filename, strp)
        else :
            for test_name in ["OUTPUT", "LINEAR", "CROP", "RAND"]:
                if test_name in ["LINEAR", "CROP", "RAND"]:
                    test_set[test_name]["FILE"] = get_sync_filename(test_set["GROUND"]["FILE"], test_name)
                test_data = test_set[test_name]
                test_filename = os.path.join(os.getcwd(), 'tests', test_data["FILE"])
                print "#### TEST:", test_name, "####\n"           
                
                ground_segments = strp.parse_ms(ground_filename)
                output_segments = strp.parse_ms(test_filename)
                matching = get_matching(ground_segments, output_segments)
                
                (PRECISION, RECALL, PRECISION_dev, RECALL_dev) = \
                    get_confusion_matrix(matching, ground_segments, output_segments)
                    
                
                
                test_data["PRECISION"] = PRECISION
                test_data["RECALL"] = RECALL
                test_data["PRECISION_dev"] = PRECISION_dev
                test_data["RECALL_dev"] = RECALL_dev
                
                
                (DIST_START, DIST_END, DIST_MID, DIST_START_dev, DIST_END_dev, DIST_MID_dev) = \
                    get_dists(matching, ground_segments, output_segments)
                test_data["DIST_START"] = DIST_START
                test_data["DIST_END"] = DIST_END
                test_data["DIST_MID"] = DIST_MID
                test_data["DIST_START_dev"] = DIST_START_dev
                test_data["DIST_END_dev"] = DIST_END_dev
                test_data["DIST_MID_dev"] = DIST_MID_dev
                
                pp.pprint(test_data)
                print ""                
                # might be useful later...
                test_data["matching"] = matching
        
    if not GENERETE_FILES:
        #print PRECISION and RECALL average    
        SUM_PRECISION_SYNCMYSUB = 0.0
        SUM_PRECISION_ANCHORPOINT = 0.0
        SUM_RECALL_SYNCMYSUB = 0.0
        SUM_RECALL_ANCHORPOINT = 0.0
        
        SUM_DSTART_SYNCMYSUB = 0.0
        SUM_DSTART_ANCHORPOINT = 0.0
        SUM_DMID_SYNCMYSUB = 0.0
        SUM_DMID_ANCHORPOINT = 0.0
        SUM_DEND_SYNCMYSUB = 0.0
        SUM_DEND_ANCHORPOINT = 0.0
        
        cont_sync_my_sub = 0.0
        cont_anchor_points = 0.0
        for movie in test_sets:
            for test_name in ["OUTPUT", "LINEAR", "CROP", "RAND"]:
                if test_name == "OUTPUT":
                    SUM_PRECISION_SYNCMYSUB += test_sets[movie][test_name]["PRECISION"]
                    SUM_RECALL_SYNCMYSUB += test_sets[movie][test_name]["RECALL"]
                    SUM_DSTART_SYNCMYSUB += test_sets[movie][test_name]["DIST_START"]
                    SUM_DMID_SYNCMYSUB += test_sets[movie][test_name]["DIST_MID"]
                    SUM_DEND_SYNCMYSUB += test_sets[movie][test_name]["DIST_END"]
                    cont_sync_my_sub += 1
                else:
                    SUM_PRECISION_ANCHORPOINT += test_sets[movie][test_name]["PRECISION"]
                    SUM_RECALL_ANCHORPOINT += test_sets[movie][test_name]["RECALL"]
                    SUM_DSTART_ANCHORPOINT += test_sets[movie][test_name]["DIST_START"]
                    SUM_DMID_ANCHORPOINT += test_sets[movie][test_name]["DIST_MID"]
                    SUM_DEND_ANCHORPOINT += test_sets[movie][test_name]["DIST_END"]
                    cont_anchor_points += 1
       
        print "SUM_PRECISION_SYNCMYSUB = ", (SUM_PRECISION_SYNCMYSUB / cont_sync_my_sub)
        print "SUM_PRECISION_ANCHORPOINT = ", (SUM_PRECISION_ANCHORPOINT / cont_anchor_points)
        print "SUM_RECALL_SYNCMYSUB = ", (SUM_RECALL_SYNCMYSUB / cont_sync_my_sub)
        print "SUM_RECALL_ANCHORPOINT = ", (SUM_RECALL_ANCHORPOINT / cont_anchor_points)
       
        print "SUM_DSTART_SYNCMYSUB = ", (SUM_DSTART_SYNCMYSUB / cont_sync_my_sub)
        print "SUM_DSTART_ANCHORPOINT = ", (SUM_DSTART_ANCHORPOINT / cont_anchor_points)
        print "SUM_DMID_SYNCMYSUB = ", (SUM_DMID_SYNCMYSUB / cont_sync_my_sub)
        print "SUM_DMID_ANCHORPOINT = ", (SUM_DMID_ANCHORPOINT / cont_anchor_points)
        print "SUM_DEND_SYNCMYSUB = ", (SUM_DEND_SYNCMYSUB / cont_sync_my_sub)
        print "SUM_DEND_ANCHORPOINT = ", (SUM_DEND_ANCHORPOINT / cont_anchor_points)
        
        #generate graphs
        gen_precision_recall_bar_graph(test_sets)
        gen_dist_bar_graph(test_sets)
            
if __name__=='__main__':
    main()
    