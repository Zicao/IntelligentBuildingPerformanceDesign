from math import pi
import matplotlib.pyplot as plt

def radar_plot(data,title='Radar'):
	"""
	"""
	Attributes =list(data.keys())
	AttNo = len(Attributes)
	values = list(data.values())
	values += values [:1]
	angles = [n / float(AttNo) * 2 * pi for n in range(AttNo)]
	angles += angles [:1]
	figureEUI=plt.figure()
	
	ax=figureEUI.add_subplot(2,2,1)
	ax = plt.subplot(111, polar=True)
	#Add the attribute labels to our axes
	plt.xticks(angles[:-1],Attributes)

	#Plot the line around the outside of the filled area, using the angles and values calculated before
	ax.plot(angles,values)

	#Fill in the area plotted in the last line
	ax.fill(angles, values, 'teal', alpha=0.1)

	#Give the plot a title and show it
	ax.set_title(title)
	plt.show()