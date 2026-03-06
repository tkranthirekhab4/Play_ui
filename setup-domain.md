# Custom Domain Setup Instructions

## Step 1: Update Windows Hosts File (Manual - Requires Admin)

1. **Open Notepad as Administrator**:
   - Right-click on Notepad
   - Select "Run as administrator"

2. **Open the hosts file**:
   - File → Open
   - Navigate to: `C:\Windows\System32\drivers\etc\hosts`
   - Set "Files of type" to "All Files (*.*)"
   - Open the "hosts" file

3. **Add the domain mapping**:
   Add this line at the end of the file:
   ```
   127.0.0.1 www.kranthitest.com
   ```

4. **Save the file**:
   - File → Save
   - Close Notepad

## Step 2: Restart Docker Container

After updating the hosts file, restart the container:

```bash
docker stop apbusbooking
docker rm apbusbooking
docker-compose up --build
```

## Step 3: Test the Domain

Open your browser and navigate to:
- http://www.kranthitest.com
- http://localhost:5000 (should still work)

## Step 4: Verify Configuration

Check that both URLs work:
- http://www.kranthitest.com → Should show your AP Bus Booking app
- http://localhost:5000 → Should show your AP Bus Booking app

## Troubleshooting

If the custom domain doesn't work:
1. Verify the hosts file was saved correctly
2. Clear your browser cache
3. Restart your browser
4. Try `ping www.kranthitest.com` in Command Prompt
5. Check if Docker container is running on port 80

## Production Domain

For a real production domain, you would need to:
1. Purchase the domain from a registrar
2. Configure DNS to point to your server's IP
3. Set up SSL certificates
4. Configure reverse proxy (nginx/Apache)
