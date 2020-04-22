import tgt
import csv
import os

directory = os.chdir("C:\\Users\\santa\\Desktop\\clean dataset\\textgrids")


################## clean up this bundle, remove unused lists:
joined_example = []
doubles_list = []
x_string_list = []
words_objects_list = []
word_list = []
list_minor_list = []
coded_segs_list = []
dataframe_list = []
dataframe_list_of_lists = []
segs_list = []
combined_segs = []
combined_segs_big_list = []
segs_lists_list = []
word_object_list = []
word_list = []

##############################################################

for file in os.listdir(directory):
    if file.endswith(".TextGrid"):
        filename = os.path.splitext(os.path.basename(file))
        tgrid = tgt.io.read_textgrid(file, encoding='utf-16')
        dataframe = tgt.io.export_to_table(tgrid)
        dataframe_list_lines = dataframe.splitlines()
        for x, item in enumerate(dataframe_list_lines):
            if x > 0:
                seg_and_prev_seg = item, dataframe_list_lines[x-1]
                seg_and_prev_seg_string = str(seg_and_prev_seg)
                seg_and_prev_seg_list = seg_and_prev_seg_string.split(',')
                seg_and_prev_seg_list.append(filename)
                if seg_and_prev_seg_list[0] == "('segments":
                    segs_lists_list.append(seg_and_prev_seg_list)
        for x in dataframe_list_lines:
            object = x.split(',')
            if object[0] == 'words':
                word_object_list.append(object)
for y in word_object_list:
    word = y[4]
    word_list.append(word)          

#print(word_list)

coded_segs_list = []

for x in segs_lists_list:
                    if '+' in str(x[4]):
                        coded_segs_list.append(x)
                    elif '#C' in str(x[4]):
                       coded_segs_list.append(x)
                    elif '#V' in str(x[4]):
                        coded_segs_list.append(x)
                    elif '#P' in str(x[4]):
                        coded_segs_list.append(x)

for (i, v) in enumerate(coded_segs_list):
     word = word_list[i]
     v.append(word)


seg_dict = {}
mini_dict = {}
seg_and_prev_seg_list = []

for x in coded_segs_list:
    coded_seg_list = []
    prev_seg_list = []
    coded_segment_object = x[4]
    code_segment_list = coded_segment_object.split("'")
    coded_segment = code_segment_list[0]
    seg_start_time = x[2]
    seg_end_time = x[3]
    seg_duration = float(seg_end_time) - float(seg_start_time)
    previous_segment_object = x[9]
    previous_segment_list = previous_segment_object.split("'")
    previous_segment = previous_segment_list[0]
    pre_seg_start_time = x[7]
    pre_seg_end_time = x[8]
    pre_seg_duration = float(pre_seg_end_time) - float(pre_seg_start_time)
    filename_string = str(x[-2])
    filename_split = filename_string.split(',')
    filename_object = str(filename_split[0])
    filename_object_split = filename_object.split("'")
    filename = filename_object_split[1]
    word = x[-1]
    coded_seg_list = [coded_segment, seg_duration, seg_start_time, seg_end_time, word, filename]
    coded_seg_list_strung = str(coded_seg_list)
    prev_seg_list = [previous_segment, pre_seg_duration, pre_seg_start_time, pre_seg_end_time, word, filename]
    prev_seg_list_strung = str(prev_seg_list)
    seg_dict[coded_seg_list_strung] = prev_seg_list_strung
    seg_and_prev_seg_list_object = coded_seg_list + prev_seg_list
    seg_and_prev_seg_list.append(seg_and_prev_seg_list_object)


#print(seg_and_prev_seg_list)


myFile = open('Python_Output.csv', 'w')
with myFile:
    writer = csv.writer(myFile)
    writer.writerows(seg_and_prev_seg_list)
    print('Python_Output')


