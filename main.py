from flask import Flask, request, send_file, render_template_string
from rembg import remove, new_session
from PIL import Image
import io
import base64
from pillow_heif import register_heif_opener

port = process.env.PORT || 4000

# Register HEIF opener
register_heif_opener()

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
            
            # Convert HEIC to RGB if necessary
            if input_image.mode != 'RGB':
                input_image = input_image.convert('RGB')
            
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
                                    <a href="https://github.com/Nishanth-Gobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                            <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                                        </svg>
                                    </a>
                                    <a href="https://www.linkedin.com/in/nishanth-gobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                                        </svg>
                                    </a>
                                    <a href="https://x.com/NishanthGobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                                        </svg>
                                    </a>
                                    <a href="https://nishanthgobi.online/" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                                        </svg>
                                    </a>
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
                                    <div id="result-container" class="relative">
                                        <img id="result-image" src="data:image/png;base64,{{ removed_bg }}" alt="Background Removed" class="w-full h-auto">
                                    </div>
                                </div>
                            </div>
                            <div class="mb-4">
                                <label class="block text-gray-700 dark:text-gray-300 text-sm font-bold mb-2" for="background-color">
                                    Choose Background Color:
                                </label>
                                <div class="flex flex-wrap gap-2">
                                    <button class="w-8 h-8 rounded-full bg-red-500" data-color="#ef4444"></button>
                                    <button class="w-8 h-8 rounded-full bg-blue-500" data-color="#3b82f6"></button>
                                    <button class="w-8 h-8 rounded-full bg-green-500" data-color="#22c55e"></button>
                                    <button class="w-8 h-8 rounded-full bg-yellow-500" data-color="#eab308"></button>
                                    <button class="w-8 h-8 rounded-full bg-purple-500" data-color="#a855f7"></button>
                                    <button class="w-8 h-8 rounded-full bg-pink-500" data-color="#ec4899"></button>
                                    <button class="w-8 h-8 rounded-full bg-gray-500" data-color="#6b7280"></button>
                                    <button class="w-8 h-8 rounded-full bg-white border border-gray-300" data-color="#ffffff"></button>
                                    <button class="w-8 h-8 rounded-full bg-black" data-color="#000000"></button>
                                </div>
                            </div>
                            <div class="text-center">
                                <a id="download-btn" href="data:image/png;base64,{{ removed_bg }}" download="background_removed.png" class="bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline transition duration-300">
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

                        // Background color change functionality
                        const resultContainer = document.getElementById('result-container');
                        const resultImage = document.getElementById('result-image');
                        const colorButtons = document.querySelectorAll('[data-color]');
                        const downloadBtn = document.getElementById('download-btn');

                        colorButtons.forEach(button => {
                            button.addEventListener('click', () => {
                                const color = button.getAttribute('data-color');
                                resultContainer.style.backgroundColor = color;
                                
                                // Create a new image with the selected background color
                                const canvas = document.createElement('canvas');
                                const ctx = canvas.getContext('2d');
                                const img = new Image();
                                img.onload = function() {
                                    canvas.width = img.width;
                                    canvas.height = img.height;
                                    ctx.fillStyle = color;
                                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                                    ctx.drawImage(img, 0, 0);
                                    
                                    // Update download link
                                    downloadBtn.href = canvas.toDataURL('image/png');
                                };
                                img.src = resultImage.src;
                            });
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
                        <a href="https://github.com/Nishanth-Gobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd" />
                            </svg>
                        </a>
                        <a href="https://www.linkedin.com/in/nishanth-gobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                            </svg>
                        </a>
                        <a href="https://x.com/NishanthGobi" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                            </svg>
                        </a>
                        <a href="https://nishanthgobi.online/" target="_blank" rel="noopener noreferrer" class="text-gray-500 hover:text-gray-600 dark:text-gray-400 dark:hover:text-gray-300">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"></path>
                            </svg>
                        </a>
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
                                <p class="text-xs text-gray-500 dark:text-gray-400">PNG, JPG, GIF, HEIC up to 10MB</p>
                            </div>
                            <input id="file-upload" name="file" type="file" class="hidden" accept="image/*,.heic" />
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

        <script src="https://cdnjs.cloudflare.com/ajax/libs/heic2any/0.0.3/heic2any.min.js"></script>
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
                    if (file.name.toLowerCase().endsWith('.heic')) {
                        // Convert HEIC to JPEG for preview
                        heic2any({
                            blob: file,
                            toType: "image/jpeg",
                            quality: 0.8
                        }).then(function(resultBlob) {
                            displayPreview(resultBlob);
                        }).catch(function (x) {
                            console.log(x);
                            alert("Error converting HEIC image. Please try another image.");
                        });
                    } else {
                        displayPreview(file);
                    }
                }
            });

            function displayPreview(blob) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    preview.classList.remove('hidden');
                }
                reader.readAsDataURL(blob);
            }

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
    app.run(debug=True, host='0.0.0.0', port=port)
