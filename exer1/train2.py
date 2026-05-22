from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.applications import MobileNetV2  # <-- Add this import
import json

dataset_dir = "C:\\Users\\mnsbartolata\\Desktop\\bartolata_fruitrecognition\\dataset"

# Data augmentation and generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    dataset_dir,
    target_size=(100, 100),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_generator = train_datagen.flow_from_directory(
    dataset_dir,
    target_size=(100, 100),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Get class names and save to JSON
fruit_classes = list(train_generator.class_indices.keys())
with open('class_indices.json', 'w') as f:
    json.dump(fruit_classes, f)

# Build the MobileNetV2-based model
base_model = MobileNetV2(input_shape=(100, 100, 3), include_top=False, weights='imagenet')
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation='relu'),
    Dense(len(fruit_classes), activation='softmax')
])

# Freeze the base model layers (optional)
base_model.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, epochs=15, validation_data=val_generator)

# Save the model
model.save('fruit_recognition_model.h5')
