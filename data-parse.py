class Object:
	def __init__ (self, mid, x_min, x_max, y_min, y_max, is_occluded, is_truncated, is_group_of, is_depiction, is_inside):
		# The class identifier for the object.
		self.mid = mid
		# Box boundaries.
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max

		# The following are booleans that provide more information about the object.

		# The object is physcally close to another object.
		self.is_occluded = is_occluded
		# The object is not fully in frame.
		self.is_truncated = is_truncated
		# Similar to is_occluded, however specifically for larger groups of objects (>5).
		self.is_group_of = is_group_of
		# Used to distinguish between a representation (e.g. a drawing or picuture) and the actual object.
		self.is_depiction = is_depiction
		# If the picture has been taken from inside the object (e.g. the picture is from inside a car).
		self.is_inside = is_inside

# Define Image class in order to store relevant information.
class Image:
	def __init__ (self, url, size, id):
		# Web URL where file is stored.
		self.url = url
		# Size of image in bytes.
		self.size = size
		# Image ID, for easy image comparison.
		self.id = id
		# Objects contained in image.
		self.objects = []

# Create dictionary to store the class descriptions.
class_descriptions = {}
# Stores all of the images for training and testing.
images = {}

print("Reading class descriptions.")
with open("resource/challenge-2019-classes-description-500.csv", "r") as f:
	lines = f.readlines()
	for l in lines:
		values = l.split(",")
		class_descriptions[values[1][:-1]] = values[0]
print(str(len(class_descriptions)) + " class descriptions read.")

print("Reading images.")
with open("resource/train-images-boxable-with-rotation.csv", "r") as f:
	# Skips first line, which are just headers.
	f.readline()

	while True:
		try:
			line = f.readline()
			if line == "":
				break

			tokens = line.split(",")
			images[tokens[0]] = Image(tokens[2], int(tokens[-4]), tokens[0])

		except Exception as e:
			print("Error reading images on line " + str(len(images)))
			continue

	print(str(len(images)) + " images read from file.")

print("Reading objects and boundary boxes.")
with open("resource/challenge-2019-train-detection-bbox.csv", "r") as f:
	lines = f.readlines()

	key_errors = 0

	for l in lines[1:]:
		tokens = l.split(",")

		for i in range(8, 13):
			if tokens[i][-1] == "\n":
				tokens[i] = tokens[i][:-1]

			if tokens[i] == "1":
				tokens[i] = True
			else:
				tokens[i] = False
		try:
			images[tokens[0]].objects.append(Object(tokens[2], float(tokens[4]), float(tokens[5]), float(tokens[6]), float(tokens[7]), tokens[8], tokens[9], tokens[10], tokens[11], tokens[12]))
		except KeyError:
			key_errors += 1

	print(str(len(lines)) + " different objects read from file.")
	print(str(key_errors) + " key errors.")
