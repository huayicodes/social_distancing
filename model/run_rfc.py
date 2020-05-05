import pickle
from rawdata_convert import load_newest_observation
# from d01_data.get_data import current
import boto3

bucket_name = "prospectparkmodel"

def run_prediction():
    print("ren_pred f initialized")
    # load data for prediction:
    try:
        data = load_newest_observation()
    except:
        print("Error: Could not read data")
        raise

    # load pkl file
    filename = 'rfc_HW.pkl'
    loaded_model = pickle.load(open(filename, 'rb'))

    # Create prediction
    # (last row of data)

    test_row = data.iloc[-1].values
    test_row = test_row.reshape(1, -1)
    pred_test = loaded_model.predict(test_row)
    output_content = str(pred_test[0])

    # Write prediction

    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, 'output.txt')
    object.put(Body=output_content)


run_prediction()





