class SparseMatrix:
    def __init__(self, file_path=None, num_rows=None, num_cols=None):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.elements = {} 
        
        if file_path:
            self.read_from_file(file_path)
    
    def read_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                self.num_rows = int(lines[0].split('=')[1].strip())
                self.num_cols = int(lines[1].split('=')[1].strip())
                
                for line in lines[2:]:
                    if line.strip():
                        if not line.startswith('(') or not line.endswith(')'):
                            raise ValueError("Input file has wrong format")
                        line = line[1:-1]  # Remove parentheses
                        parts = line.split(',')
                        if len(parts) != 3:
                            raise ValueError("Input file has wrong format")
                        
                        row = int(parts[0].strip())
                        col = int(parts[1].strip())
                        value = int(parts[2].strip())
                        self.elements[(row, col)] = value
        
        except Exception as e:
            raise ValueError("Input file has wrong format") from e
    
    def get_element(self, row, col):
        return self.elements.get((row, col), 0)
    
    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]
    
    def add(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must be the same for addition")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        for key in self.elements.keys() | other.elements.keys():
            result.set_element(key[0], key[1], self.get_element(*key) + other.get_element(*key))
        
        return result
    
    def subtract(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must be the same for subtraction")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=self.num_cols)
        
        for key in self.elements.keys() | other.elements.keys():
            result.set_element(key[0], key[1], self.get_element(*key) - other.get_element(*key))
        
        return result
    
    def multiply(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Number of columns of the first matrix must equal the number of rows of the second matrix")
        
        result = SparseMatrix(num_rows=self.num_rows, num_cols=other.num_cols)
        
        for (i, k) in self.elements.keys():
            for j in range(other.num_cols):
                result.set_element(i, j, result.get_element(i, j) + self.get_element(i, k) * other.get_element(k, j))
        
        return result

def main():
    import sys
    if len(sys.argv) != 4:
        print("Usage: python sparse_matrix.py <operation> <matrix_file1> <matrix_file2>")
        return
    
    operation = sys.argv[1]
    file1 = sys.argv[2]
    file2 = sys.argv[3]
    
    matrix1 = SparseMatrix(file_path=file1)
    matrix2 = SparseMatrix(file_path=file2)
    
    result = None
    
    if operation == "add":
        result = matrix1.add(matrix2)
    elif operation == "subtract":
        result = matrix1.subtract(matrix2)
    elif operation == "multiply":
        result = matrix1.multiply(matrix2)
    else:
        print("Invalid operation. Use 'add', 'subtract', or 'multiply'")
        return
    
    print(result)

if __name__ == "__main__":
    main()
