import json
import pandas as pd
import modelop.utils as utils
from pathlib import Path

logger = utils.configure_logger()

#
# This method gets called when the monitor is loaded by the ModelOp runtime. It sets the GLOBAL values that are
# extracted from the report.txt to obtain the DTS and version info to append to the report
#

# modelop.init
def init(init_param):
	logger = utils.configure_logger()

#
# This method is the modelops metrics method.  This is always called with a pandas dataframe that is arraylike, and
# contains individual rows represented in a dataframe format that is representative of all of the data that comes in
# as the results of the first input asset on the job.  This method will not be invoked until all data has been read
# from that input asset.
#
# For this example, we simply echo back the first row of that data as a json object.  This is useful for things like
# reading externally generated metrics from an SQL database or an S3 file and having them interpreted as a model test
# result for the association of these results with a model snapshot.
#
# data - The input data of the first input asset of the job, as a pandas dataframe
#

# modelop.metrics
def metrics(data: pd.DataFrame):
	logger.info("Running the metrics function")

	finalResult = {}
	if data.empty:
		logger.info("No input data provided")
		finalResult["sample"] = {"no": "data provided"}
	else:
		finalResult["input_data"] = data.iloc[0].to_dict()
		finalResult["generic_graph"] = {"title" : "Example Horizontal Bar Chart", "x_axis_label": "X Axis", "y_axis_label": "Y Axis", "axis_min_default": -1, "axis_max_default":2.6, "data": { "data1": [1, 2, 3, 4], "data2": [4, 3, 2, 1] }, "categories": ["cat1", "cat2", "cat3", "cat4"]}
		finalResult["generic_table"] = [{"data1": 1, "data2": 2, "data3" : 3}, {"data1": 2, "data2" : 3, "data3": 4}, {"data1":  3, "data2": 4, "data3" : 5}]
		finalResult["generic_line_graph"] = {"title": "Example Line Graph - XY Data", "x_axis_label": "X Axis", "y_axis_label": "Y Axis", "data": {"data1": [[1,100], [3,200], [5, 300]], "data2": [[2, 350], [4, 250], [6, 150]] } }

	yield finalResult

#
# This main method is utilized to simulate what the engine will do when calling the above metrics function.  It takes
# the json formatted data, and converts it to a pandas dataframe, then passes this into the metrics function for
# processing.  This is a good way to develop your models to be conformant with the engine in that you can run this
# locally first and ensure the python is behaving correctly before deploying on a ModelOp engine.
#
def main():

	raw_json = Path('example_job.json').read_text()
	init_param = {'rawJson': raw_json}

	init(init_param)
	df = pd.read_csv('german_credit_data.csv')
	print(df)
	# data = '''
	#  	{"id":993,"duration_months":36,"credit_amount":3959,"installment_rate":4,"present_residence_since":3,"age_years":30,"number_existing_credits":1,"checking_status":"A11","credit_history":"A32","purpose":"A42","savings_account":"A61","present_employment_since":"A71","debtors_guarantors":"A101","property":"A122","installment_plans":"A143","housing":"A152","job":"A174","number_people_liable":1,"telephone":"A192","foreign_worker":"A201","gender":"male","label_value":0,"score":1}
	#  '''
	# data_dict = json.loads(data)
	# df = pd.DataFrame.from_dict([data_dict])
	print(json.dumps(next(metrics(df)), indent=2))


if __name__ == '__main__':
	main()
