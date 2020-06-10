def calc(data, rpack):
	equation = data[0].lower().replace("plus", "+").replace("minus", "-")
	equation = equation.replace("^", "**").replace("x", "*").replace(",", ".")
	return eval(equation), rpack

