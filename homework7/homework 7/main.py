import os
import requests
import fitz

# Bot token and channel ID
bot_token = "7223921695:AAHg9mz6FNEk6FKjINnKntfcoL7GhPLXXEQ"
channel_username = "@maabtask7channel"
api_url = f"https://api.telegram.org/bot{bot_token}"

# Folder containing the PDF books
books_folder = r"D:\books"

def post_books():
    for file_name in os.listdir(books_folder):
        if file_name.lower().endswith(".pdf"):
            book_path = os.path.join(books_folder, file_name)

            # Open the PDF and extract the first page as an image using PyMuPDF
            with fitz.open(book_path) as pdf_document:
                first_page = pdf_document.load_page(0)
                pix = first_page.get_pixmap()
                image_path = os.path.join(books_folder, f"{file_name}_first_page.png")
                pix.save(image_path)

            # Send the image to the Telegram channel
            with open(image_path, "rb") as image_file:
                response = requests.post(f"{api_url}/sendPhoto",
                    data={"chat_id": channel_username},
                    files={"photo": image_file}
                )
                if response.status_code == 200:
                    message_id = response.json()["result"]["message_id"]

                    # Send the PDF file as a reply to the image message
                    with open(book_path, "rb") as pdf_file:
                        requests.post(
                            f"{api_url}/sendDocument",
                            data={
                                "chat_id": channel_username,
                                "reply_to_message_id": message_id,
                            },
                            files={"document": pdf_file}
                        )
                    print(f"Posted {file_name} to the channel.")
                else:
                    print(f"Failed to post image for {file_name}: {response.text}")

            # Remove the temporary image file
            os.remove(image_path)

# Run the function
post_books()
