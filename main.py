from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
def health():
    return {"ok": True}


#@app.post("/webhook")
#def webhook(uid: str, transcript: dict):
# def webhook(data: dict):
#     print(data)
#     #print(transcript)

#     # Extract uid and transcript from the request body
#     uid = data.get("uid", "unknown")
#     transcript = data.get("transcript", {})

#     # Hint: The transcript contains segments with text data
#     # Hint: Access the latest segment with transcript["segments"][-1]["text"]
#     # Hint: Return a dictionary with a "message" key and the value being the notification message

#     # Task: Implement keyword detection and response logic of your choice
#     # example: if the word "tired" is mentioned, return a message notifying the user to take a break

#     # Write your code below this line
#     if "segments" in transcript and len(transcript["segments"]) > 0:
#         latest_text = transcript["segments"][-1]["text"].lower()
        
#         # Check for keywords
#         if "tired" in latest_text:
#             return {"message": "You mentioned being tired. Consider taking a break!"}
#         elif "help" in latest_text:
#             return {"message": "I heard you need help. How can I assist you?"}
#         elif "urgent" in latest_text:
#             return {"message": "This sounds urgent! Please prioritize this task."}
    
#     # Default response if no keywords detected
#     return {"message": "Transcript received successfully"}

@app.post("/webhook")
def webhook(data: dict):
    print("Full data received:", data)
    
    # OMI sends segments directly, not under 'transcript'
    segments = data.get("segments", [])
    print("Segments found:", segments)
    
    # Check if we have segments
    if segments and len(segments) > 0:
        # Get the latest segment
        latest_segment = segments[-1]
        print("Latest segment:", latest_segment)
        
        # Check if it's a dictionary with 'text' key
        if isinstance(latest_segment, dict) and "text" in latest_segment:
            latest_text = latest_segment["text"].lower()
            print("Latest text:", latest_text)
            
            # Check for keywords
            if "tired" in latest_text:
                response = {"message": "You mentioned being tired. Consider taking a break!"}
                print("Returning response:", response)
                return response
            elif "help" in latest_text:
                response = {"message": "I heard you need help. How can I assist you?"}
                print("Returning response:", response)
                return response
            elif "urgent" in latest_text:
                response = {"message": "This sounds urgent! Please prioritize this task."}
                print("Returning response:", response)
                return response
        else:
            print("Latest segment is not a proper dictionary or missing 'text' key")
            response = {"message": "Invalid transcript format received"}
            print("Returning response:", response)
            return response
    
    # Default response if no keywords detected
    response = {"message": "Transcript received successfully"}
    print("Returning response:", response)
    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

