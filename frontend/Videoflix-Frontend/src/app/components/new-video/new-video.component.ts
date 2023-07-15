import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { VideoService } from 'src/app/services/video.service';

@Component({
  selector: 'app-new-video',
  templateUrl: './new-video.component.html',
  styleUrls: ['./new-video.component.scss']
})
export class NewVideoComponent implements OnInit {

  videos: any[] = [];

  selectedVideo: any = null;

  title!: string;
  description!: string;
  videofile!: any;

  inputTitle: string = '';
  inputDescription: string = '';

  constructor(private router: Router, private videoService: VideoService) { }

  ngOnInit(): void {
    this.subscribeToVideoService();
    this.videoService.getVideos();
  }

  subscribeToVideoService() {
    this.videoService.videos$.subscribe(videos => {
      this.videos = videos;
    });
  }

  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
        this.videofile = event.target.files[0];
    }
}

async uploadVideo(){
  const data = new FormData();
  data.append('created_from', localStorage.getItem('username') || '');
  data.append('title', this.title);
  data.append('description', this.description);
  data.append('video_file', this.videofile);

  const requestOptions : RequestInit = {
      method: 'POST',
      body: data
  };

  try {
      const response = await fetch("https://googlec-videoflix.niels-scholz.com/v1/videos/", requestOptions);

      if (response.ok) {
          const result = await response.json();
          console.log(result);
          this.router.navigate(['/startsite']);
          setTimeout(() => {
            window.location.reload();
          }, 1000);
      } else {
          const errorResponse = await response.json();
          console.log('Error:', errorResponse);
      }
  } catch (error) {
      console.log('error', error);
  }
}

selectVideo(video: any) {
  this.selectedVideo = video;
  this.inputTitle = video.title;
  this.inputDescription = video.description;
  document.getElementById('all-your-videos')?.classList.add('d-none');
  document.getElementById('new-video-button')?.classList.add('d-none');
}

unselectVideo(){
  this.selectedVideo = null;
  document.getElementById('all-your-videos')?.classList.remove('d-none');
  document.getElementById('new-video-button')?.classList.remove('d-none');
}

async updateVideoInformations() {
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const raw = JSON.stringify({
    "title": this.inputTitle,
    "description": this.inputDescription
  });

  const requestOptions : RequestInit = {
    method: 'PATCH',
    headers: myHeaders,
    body: raw,
  };

  await fetch(`https://googlec-videoflix.niels-scholz.com/v1/videos/${this.selectedVideo.id}/`, requestOptions)
    .then(response => response.json())
    .then(result => {
      console.log(result)
      this.selectedVideo.title = this.inputTitle;
      this.selectedVideo.description = this.inputDescription;
      this.unselectVideo();
    })
    .catch(error => console.log('error', error));
}

async deleteVideo() {
  const myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  const requestOptions : RequestInit = {
    method: 'DELETE',
    headers: myHeaders,
  };

  await fetch(`https://googlec-videoflix.niels-scholz.com/v1/videos/${this.selectedVideo.id}/`, requestOptions)
    .then(response => {
      if (response.ok) {
        console.log('Video erfolgreich gelöscht');
        this.unselectVideo();
        window.location.reload();
      } else {
        throw new Error('Fehler beim Löschen des Videos');
      }
    })
    .catch(error => console.log('error', error));
}

  switchContainerUploadNewVideo(){
    document.getElementById('all-your-videos')?.classList.add('d-none');
    document.getElementById('new-video-button')?.classList.add('d-none');
    document.getElementById('upload-new-video')?.classList.remove('d-none-mobile');
  }

  switchContainerBackUploadNewVideo(){
    document.getElementById('all-your-videos')?.classList.remove('d-none');
    document.getElementById('new-video-button')?.classList.remove('d-none');
    document.getElementById('upload-new-video')?.classList.add('d-none-mobile');
  }

}
