from static.detection_part.test_PE_analytics import start_detect,get_output_path,get_output_filename

def predict(path,model,total_pallet):
    # detection part => xlsx file
    start_detect(path,model, saved=False)
    result_path = get_output_path()
    print(f'output has been save as : {result_path}')
    return get_output_filename()


