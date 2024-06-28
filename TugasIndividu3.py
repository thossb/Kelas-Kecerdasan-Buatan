from constraint import *

# Inisialisasi solver CSP
problem = Problem()

# Daftar daerah pada peta
areas = ['A', 'B', 'C', 'D']

# Setiap daerah harus diberi warna merah, hijau, atau biru
colors = ['red', 'green', 'blue']

# Tambahkan variabel-variabel ke solver CSP
for area in areas:
    problem.addVariable(area, colors)

# Setiap daerah yang bersebelahan tidak boleh memiliki warna yang sama
problem.addConstraint(lambda a, b: a != b, ('A', 'B'))
problem.addConstraint(lambda a, b: a != b, ('A', 'C'))
problem.addConstraint(lambda a, b: a != b, ('B', 'D'))
problem.addConstraint(lambda a, b: a != b, ('C', 'D'))

# Solusi dari CSP
solutions = problem.getSolutions()

# Cetak hasil solusi
for solution in solutions:
    print(solution)
