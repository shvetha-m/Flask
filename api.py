from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import ast
import pandas as pd

app = Flask(__name__)
api = Api(app)


STUDENTS = {
  '1': {'name': 'Mark', 'age': 23, 'spec': 'math'},
  '2': {'name': 'Jane', 'age': 20, 'spec': 'biology'},
  '3': {'name': 'Peter', 'age': 21, 'spec': 'history'},
  '4': {'name': 'Kate', 'age': 22, 'spec': 'science'},
}

Number_list = [1,2,3,4,5,6]

parser = reqparse.RequestParser()

class StudentsList(Resource):
    def get(self):
        return STUDENTS

  
    def post(self):
        parser.add_argument("name")
        parser.add_argument("age")
        parser.add_argument("spec")
        args = parser.parse_args()
        student_id = int(max(STUDENTS.keys())) + 1
        student_id = '%i' % student_id
        STUDENTS[student_id] = {
            "name": args["name"],
            "age": args["age"],
            "spec": args["spec"],
         }
        return STUDENTS[student_id], 201

class Min(Resource):
    def get(self):
        n = request.args['quantifier'] 
        op = request.args['numlist']   
        x =  ast.literal_eval(op)    
        output = []
        Number_list.sort()
        for i in range(int(n)):
            output.append(x[i])
        return output

class Max(Resource):
    def get(self):
        n = request.args['quantifier'] 
        op = request.args['numlist']   
        x =  ast.literal_eval(op)    
        output = []
        x.sort()
        x = x[::-1]
        for i in range(int(n)):
            output.append(x[i])
        return output

class Avg(Resource):
    def get(self):
        op = request.args['numlist']
        x =  ast.literal_eval(op)   
        return sum(x)/len(x)

class Median(Resource):
    def get(self):
        op = request.args['numlist']
        x =  ast.literal_eval(op)  
        x.sort()
        mid = len(x) // 2
        res = (x[mid] + x[~mid]) / 2
        return res

class Percentile(Resource):
    def get(self):
        op = request.args['numlist']
        percentile = int(request.args['quantifier'])
        x =  ast.literal_eval(op)  
        x = pd.Series(x)
        res = x.quantile(percentile/100)
        return res


api.add_resource(StudentsList, '/students/')
api.add_resource(Min, '/min/')
api.add_resource(Max, '/max/')
api.add_resource(Avg, '/avg/')
api.add_resource(Median, '/median/')
api.add_resource(Percentile, '/percentile/')


if __name__ == "__main__":
  app.run(debug=True)

