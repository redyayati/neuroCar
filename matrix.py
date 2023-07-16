import random 

class Matrix(): 
    def __init__(self,numR,numC) : 
        self.rows = numR
        self.cols = numC
        self.data = [[0 for i in range(self.cols)] for j in range(self.rows)]
    def copy(self) : 
        newMat = Matrix(self.rows,self.cols)
        for i in range(self.rows): 
            for j in range(self.cols) : 
                newMat.data[i][j] = self.data[i][j]
        return newMat
    def add(self,n) : 
        if type(n) == type(self) : 
            for i in range(self.rows) :
                for j in range(self.cols):
                    self.data[i][j] += n.data[i][j]
        else : 
            for i in range(self.rows) :
                for j in range(self.cols):
                    self.data[i][j] += n 
    @staticmethod
    def substract(m1,m2) : 
        result = Matrix(m1.rows, m1.cols)
        for i in range(m1.rows) :
            for j in range(m1.cols):
                result.data[i][j] = m1.data[i][j] - m2.data[i][j]
        return result
                
    def randomize(self):
        for i in range(self.rows) :
            for j in range(self.cols):
                self.data[i][j] = random.uniform(-1,1)
    @staticmethod
    def toMatrix(inputs) : 
        rows = len(inputs)
        cols = 1
        result = Matrix(rows,cols)
        for i in range(rows) : 
            for j in range(cols) : 
                result.data[i][j] = inputs[i]
        return result
    @staticmethod
    def fromMatrix(matrix) : 
        data = matrix.data
        result = [] 
        rows = len(matrix.data)
        cols = 1
        for i in range(rows) : 
            for j in range(cols) : 
                result.append(data[i][j])
        return result 

    
    @staticmethod
    def multiply(m1,m2) : 
        if type(m1) == type(m2) : 
            result = Matrix(m1.rows,m2.cols)
            if m1.cols == m2.rows : 
                for row in range(m1.rows) : 
                    for col in range(m2.cols) : 
                        for i in range(m1.cols) : 
                            result.data[row][col] += m1.data[row][i] * m2.data[i][col]
                return result
            else : 
                print("cannot be multiplied")
                return
    def multiplyn(self,m2) : 
        if type(self) == type(m2) : 
            # hadamard product
            for row in range(self.rows) : 
                for col in range(m2.cols) : 
                    self.data[row][col] *= m2.data[row][col]
        else : 
            for i in range(self.rows) :
                for j in range(self.cols):
                    self.data[i][j] *= m2
    @staticmethod
    def transpose(m) : 
        result = Matrix(m.cols,m.rows)
        for row in range(m.rows) : 
            for col in range(m.cols) : 
                result.data[col][row] = m.data[row][col]
        return result
    @staticmethod
    def addin(m1, m2) : 
        rows = m1.rows
        cols = m1.cols
        result = Matrix(rows,cols)
        for i in range(rows) :  
            for j in range(cols) : 
                result.data[i][j] = m1.data[i][j] + m2.data[i][j]
        return result
    def zap(self,func) : 
        rows = self.rows
        cols = self.cols
        for i in range(rows) :  
            for j in range(cols) : 
                val = self.data[i][j]
                self.data[i][j] = func(val)
    @staticmethod
    def zapn(mat,func) : 
        rows = mat.rows
        cols = mat.cols
        result = Matrix(rows,cols)
        for i in range(rows) :  
            for j in range(cols) : 
                result.data[i][j] = func(mat.data[i][j])
        return result


# a= Matrix(3,1)
# a.randomize()
# b= Matrix(1,3)
# b.randomize()
# print(a.data)
# print(b.data)
# # # c = Matrix.multiply(a,b)
# # # print(c.data)
# # # a.multiplyn(3)
# # print(a.data)

# # def doubleit(x) : 
# #     return x*2 
# # a.zap(doubleit)
# # print(a.data)

# test = [1,2,3,4,5]
# m = Matrix.toMatrix(test)
# print(m.data)

# # n = Matrix.fromMatrix(a)
# # print("dfg")
# # print(n)

# c = Matrix.multiply(a,b)
# print(c.data)