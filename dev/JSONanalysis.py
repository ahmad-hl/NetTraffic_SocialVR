import json, os
from pandas import json_normalize

#input files
file_names = ['2_9zR9fdn.json'] #'2tabs-f9Fsp7W.json', '4tabs-zuyDZuT.json', '8tabs-SXKzC2s.json', '16tabs-9V3umQ4.json'
# file_names = ['2tabs-TbACBYQ.json', '4tabs-q8giDem.json', '6tabs-uVoyVox.json', '20tabs-wyfT6CL.json']
dir_name = 'synth3'
# dir_name = 'synth'

for file_name in file_names:
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    curr_dir = os.path.join(curr_dir, '..', dir_name)
    json_path = os.path.join(curr_dir, file_name)

    infile = open(json_path, 'r',encoding='utf-8')
    json_string = infile.read()
    print(json_string +'\n')
    data = json.loads(json_string)
    data_body = data['body']
    print(data_body)
    data = json.loads(data_body)
    items = data['data']['Items']
    count = data['data']['Count']
    scannedCount = data['data']['ScannedCount']
    print("count: {}, scannedCount: {}, items: {} \n ********* \n".format(count, scannedCount,  items))

    # for idx in range(len(items)):
    #     print(items[idx])
    print("\n ********* \n")
    # Use json_normalize() to convert JSON to DataFrame
    loadTimeDF = json_normalize(data['data']['Items'])
    print(loadTimeDF)

    try:
        tabs_number = int(file_name[0:2])
    except:
        tabs_number = int(file_name[0:1])
    loadTimeDF.to_csv(r'{}/room_access_{}.csv'.format(curr_dir, tabs_number), encoding='utf-8', mode='w', index=False, header=True)



