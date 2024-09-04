from flask import Flask, request, send_file, render_template_string
from rembg import remove, new_session
from PIL import Image
import io
import base64

app = Flask(__name__)

# Create a session with a more advanced model
session = new_session("u2net")

@app.route('/', methods=['GET', 'POST'])
def remove_background():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file', 400
        
        if file:
            # Read the image file
            input_image = Image.open(file.stream)
            
            # Remove the background
            output_image = remove(
                input_image,
                session=session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Convert images to base64 for display
            buffered = io.BytesIO()
            input_image.save(buffered, format="PNG")
            original_image_base64 = base64.b64encode(buffered.getvalue()).decode()

            buffered = io.BytesIO()
            output_image.save(buffered, format="PNG")
            removed_bg_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            return render_template_string('''
                <!doctype html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>BG Begone</title>
                    <script src="https://cdn.tailwindcss.com"></script>
                    <script>
                        tailwind.config = {
                            darkMode: 'class',
                            theme: {
                                extend: {
                                    colors: {
                                        primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a"}
                                    }
                                },
                                fontFamily: {
                                    'body': [
                                        'Inter', 
                                        'ui-sans-serif', 
                                        'system-ui', 
                                        '-apple-system', 
                                        'system-ui', 
                                        'Segoe UI', 
                                        'Roboto', 
                                        'Helvetica Neue', 
                                        'Arial', 
                                        'Noto Sans', 
                                        'sans-serif', 
                                        'Apple Color Emoji', 
                                        'Segoe UI Emoji', 
                                        'Segoe UI Symbol', 
                                        'Noto Color Emoji'
                                    ],
                                    'sans': [
                                        'Inter', 
                                        'ui-sans-serif', 
                                        'system-ui', 
                                        '-apple-system', 
                                        'system-ui', 
                                        'Segoe UI', 
                                        'Roboto', 
                                        'Helvetica Neue', 
                                        'Arial', 
                                        'Noto Sans', 
                                        'sans-serif', 
                                        'Apple Color Emoji', 
                                        'Segoe UI Emoji', 
                                        'Segoe UI Symbol', 
                                        'Noto Color Emoji'
                                    ]
                                }
                            }
                        }
                    </script>
                </head>
                <body class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white transition-colors duration-300">
                    <nav class="bg-white dark:bg-gray-800 shadow-lg">
                        <div class="max-w-7xl mx-auto px-4">
                            <div class="flex justify-between">
                                <div class="flex space-x-7">
                                    <div>
                                        <a href="/" class="flex items-center py-4 px-2">
                                            <span class="font-semibold text-gray-500 dark:text-gray-300 text-lg">BG Begone</span>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center space-x-3">
                                    <button id="darkModeToggle" class="p-2 rounded-full bg-gray-200 dark:bg-gray-700">
                                        <svg class="w-6 h-6 text-gray-800 dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </nav>

                    <div class="container mx-auto px-4 py-8">
                        <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md max-w-4xl mx-auto">
                            <h1 class="text-2xl font-bold mb-6 text-center text-gray-800 dark:text-white">Background Removal Result</h1>
                            <div class="flex flex-col md:flex-row justify-between mb-6">
                                <div class="w-full md:w-1/2 p-2">
                                    <h2 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Original Image</h2>
                                    <img src="data:image/png;base64,{{ original_image }}" alt="Original Image" class="w-full h-auto">
                                </div>
                                <div class="w-full md:w-1/2 p-2">
                                    <h2 class="text-lg font-semibold mb-2 text-gray-800 dark:text-white">Background Removed</h2>
                                    <img src="data:image/png;base64,{{ removed_bg }}" alt="Background Removed" class="w-full h-auto">
                                </div>
                            </div>
                            <div class="text-center">
                                <a href="data:image/png;base64,{{ removed_bg }}" download="background_removed.png" class="bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300">
                                    Download Processed Image
                                </a>
                            </div>
                        </div>
                    </div>

                    <script>
                        const html = document.querySelector('html');
                        const darkModeToggle = document.getElementById('darkModeToggle');

                        // Function to set the theme
                        function setTheme(theme) {
                            if (theme === 'dark') {
                                html.classList.add('dark');
                            } else {
                                html.classList.remove('dark');
                            }
                            localStorage.theme = theme;
                        }

                        // Check for saved theme preference or use system preference
                        if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                            setTheme('dark');
                        } else {
                            setTheme('light');
                        }

                        // Dark mode toggle
                        darkModeToggle.addEventListener('click', () => {
                            if (html.classList.contains('dark')) {
                                setTheme('light');
                            } else {
                                setTheme('dark');
                            }
                        });
                    </script>
                </body>
                </html>
            ''', original_image=original_image_base64, removed_bg=removed_bg_base64)
    
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>BG Begone</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script>
            tailwind.config = {
                darkMode: 'class',
                theme: {
                    extend: {
                        colors: {
                            primary: {"50":"#eff6ff","100":"#dbeafe","200":"#bfdbfe","300":"#93c5fd","400":"#60a5fa","500":"#3b82f6","600":"#2563eb","700":"#1d4ed8","800":"#1e40af","900":"#1e3a8a"}
                        }
                    },
                    fontFamily: {
                        'body': [
                            'Inter', 
                            'ui-sans-serif', 
                            'system-ui', 
                            '-apple-system', 
                            'system-ui', 
                            'Segoe UI', 
                            'Roboto', 
                            'Helvetica Neue', 
                            'Arial', 
                            'Noto Sans', 
                            'sans-serif', 
                            'Apple Color Emoji', 
                            'Segoe UI Emoji', 
                            'Segoe UI Symbol', 
                            'Noto Color Emoji'
                        ],
                        'sans': [
                            'Inter', 
                            'ui-sans-serif', 
                            'system-ui', 
                            '-apple-system', 
                            'system-ui', 
                            'Segoe UI', 
                            'Roboto', 
                            'Helvetica Neue', 
                            'Arial', 
                            'Noto Sans', 
                            'sans-serif', 
                            'Apple Color Emoji', 
                            'Segoe UI Emoji', 
                            'Segoe UI Symbol', 
                            'Noto Color Emoji'
                        ]
                    }
                }
            }
        </script>
    </head>
    <body class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white transition-colors duration-300">
        <nav class="bg-white dark:bg-gray-800 shadow-lg">
            <div class="max-w-7xl mx-auto px-4">
                <div class="flex justify-between">
                    <div class="flex space-x-7">
                        <div>
                            <a href="/" class="flex items-center py-4 px-2">
                                <span class="font-semibold text-gray-500 dark:text-gray-300 text-lg">BG Begone</span>
                            </a>
                        </div>
                    </div>
                    <div class="flex items-center space-x-3">
                        <button id="darkModeToggle" class="p-2 rounded-full bg-gray-200 dark:bg-gray-700">
                            <svg class="w-6 h-6 text-gray-800 dark:text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="container mx-auto px-4 py-8">
            <div class="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-md max-w-md mx-auto">
                <h1 class="text-2xl font-bold mb-6 text-center text-gray-800 dark:text-white">Remove Image Background</h1>
                <form id="upload-form" method="post" enctype="multipart/form-data" class="space-y-4">
                    <div class="flex items-center justify-center w-full">
                        <label for="file-upload" class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 dark:border-gray-600 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600">
                            <div class="flex flex-col items-center justify-center pt-5 pb-6">
                                <svg class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                                <p class="mb-2 text-sm text-gray-500 dark:text-gray-400"><span class="font-semibold">Click to upload</span> or drag and drop</p>
                                <p class="text-xs text-gray-500 dark:text-gray-400">PNG, JPG, GIF up to 10MB</p>
                            </div>
                            <input id="file-upload" name="file" type="file" class="hidden" />
                        </label>
                    </div>
                    <div id="preview" class="hidden">
                        <img id="preview-image" src="" alt="Preview" class="w-full h-64 object-contain mb-4">
                    </div>
                    <div>
                        <button id="submit-btn" type="submit" class="w-full bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300">
                            Remove Background
                        </button>
                    </div>
                </form>
                <div id="spinner" class="hidden flex justify-center items-center mt-4">
                    <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
                </div>
            </div>
        </div>

        <script>
            const html = document.querySelector('html');
            const darkModeToggle = document.getElementById('darkModeToggle');
            const fileUpload = document.getElementById('file-upload');
            const preview = document.getElementById('preview');
            const previewImage = document.getElementById('preview-image');
            const form = document.getElementById('upload-form');
            const submitBtn = document.getElementById('submit-btn');
            const spinner = document.getElementById('spinner');

            // Function to set the theme
            function setTheme(theme) {
                if (theme === 'dark') {
                    html.classList.add('dark');
                } else {
                    html.classList.remove('dark');
                }
                localStorage.theme = theme;
            }

            // Check for saved theme preference or use system preference
            if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                setTheme('dark');
            } else {
                setTheme('light');
            }

            // Dark mode toggle
            darkModeToggle.addEventListener('click', () => {
                if (html.classList.contains('dark')) {
                    setTheme('light');
                } else {
                    setTheme('dark');
                }
            });

            // File upload preview
            fileUpload.addEventListener('change', function(event) {
                const file = event.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        previewImage.src = e.target.result;
                        preview.classList.remove('hidden');
                    }
                    reader.readAsDataURL(file);
                }
            });

            // Form submission
            form.addEventListener('submit', function(event) {
                event.preventDefault();
                spinner.classList.remove('hidden');
                submitBtn.disabled = true;
                submitBtn.classList.add('opacity-50', 'cursor-not-allowed');
                this.submit();
            });
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
