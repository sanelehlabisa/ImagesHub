import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';

@Component({
  selector: 'app-image-details',
  templateUrl: './image-details.component.html',
  styleUrls: ['./image-details.component.css']
})
export class ImageDetailsComponent {
  constructor(
    @Inject(MAT_DIALOG_DATA) public data: { imageUrl: string, filename: string },
    private dialogRef: MatDialogRef<ImageDetailsComponent> // Inject MatDialogRef
  ) {}

  async downloadImage(): Promise<void> {
    try {
      const response = await fetch(this.data.imageUrl);
      const blob = await response.blob();
      const a = document.createElement('a');
      const blobUrl = URL.createObjectURL(blob);
      
      a.href = blobUrl; // Use the Blob URL for downloading
      a.download = this.data.filename || 'download'; // Set the filename for download
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
      // Clean up the Blob URL
      URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error('Error downloading file:', error);
    }
  }

  close(): void {
    this.dialogRef.close(); // Close the dialog
  }
}
