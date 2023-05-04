import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '@app/_models';
import { AccountService } from '@app/_services';

@Component({ 
    templateUrl: 'home.component.html',
})
export class HomeComponent {
    user: User | null;
    selectedFile!: File;
    selectedFileName!: string;
    myFile: any = null;
    fileName: string = '';
    file1!: File;
    file2!: File;

    constructor(private accountService: AccountService, private http: HttpClient) {
      this.user = this.accountService.userValue;
      this.file1;
      this.file2;
    }
  
    onFileChange(event: any, fileType: string) {
      const fileList: FileList = event.target.files;
      if (fileList.length > 0) {
        if (fileType === 'file1') {
          this.file1 = fileList[0];
        } else if (fileType === 'file2') {
          this.file2 = fileList[0];
        }
      }
    }
  
    onSubmit() {
      if (!this.file1 || !this.file2) {
        alert("Please select both files to upload.");
        return;
      }
  
      const formData: FormData = new FormData();
      formData.append('file1', this.file1, this.file1.name);
      formData.append('file2', this.file2, this.file2.name);
  
      // Make the HTTP request
      this.http.post('http://127.0.0.1:5000', formData)
        .subscribe(
          response => {
            console.log('Upload successful!', response);
            // Add any further logic or display success message here
          },
          error => {
            console.error('Error occurred during file upload!', error);
            // Handle error and display error message here
          }
        );
    }

    uploadFiles(formData: FormData) {
      // Make the HTTP request
      // Replace 'https://example.com/upload' with your actual upload endpoint URL
      fetch('http://127.0.0.1:5000', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (response.ok) {
          console.log('Files uploaded successfully!');
        } else {
          console.error('Error occurred during file upload!');
        }
      })
      .catch(error => {
        console.error('Error occurred during file upload!', error);
      });
    }
}

