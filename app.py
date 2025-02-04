import os
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request, jsonify
from cloudinary.utils import cloudinary_url

# Load Cloudinary credentials from environment variables
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dihlrlise"),  # Default value for testing
    api_key=os.getenv("CLOUDINARY_API_KEY", "262784859187517"),  # Default value for testing
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "3WjQkfwEpl8WaCrq67-8RrWMH2o"),  # Default value for testing
    secure=True
)

# Initialize Flask app
app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']  # The uploaded image file
    if not file:
        return jsonify({"error": "No image uploaded"}), 400

    # Upload image to Cloudinary
    upload_result = cloudinary.uploader.upload(file)
    uploaded_image_url = upload_result["secure_url"]
    
    # Generate optimized image URL
    optimize_url, _ = cloudinary_url(upload_result["public_id"], fetch_format="auto", quality="auto")
    
    # Generate auto-cropped image URL
    auto_crop_url, _ = cloudinary_url(upload_result["public_id"], width=500, height=500, crop="auto", gravity="auto")
    
    # Return the URLs of the images
    return jsonify({
        "uploaded_image": uploaded_image_url,
        "optimized_image": optimize_url,
        "auto_cropped_image": auto_crop_url
    })

if __name__ == '__main__':
    # Use host='0.0.0.0' and port from the environment (for cloud platforms)
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
