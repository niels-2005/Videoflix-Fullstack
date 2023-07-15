import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { StartsiteService } from 'src/app/services/startsite.service';
import { VideoService } from 'src/app/services/video.service';

@Component({
  selector: 'app-startsite',
  templateUrl: './startsite.component.html',
  styleUrls: ['./startsite.component.scss']
})
export class StartsiteComponent implements OnInit {

  videos: any[] = [];
  searchTerm: string = '';

  showQualityMenu = false;
  isFullscreen = false;

  showDropdown = false;

  selectedVideo: any = null;

  constructor(private startsiteService: StartsiteService, private videoService: VideoService) {}

  ngOnInit(): void {
    this.subscribeToStartsiteService();
    this.subscribeToVideoService();
    this.videoService.getVideos();
  }

  subscribeToStartsiteService() {
    this.startsiteService.showAllVideos$.subscribe(show => {
      const startsiteAllVideos = document.getElementById('startsite-all-videos');
      if (show) {
        startsiteAllVideos?.classList.remove('d-none');
      } else {
        startsiteAllVideos?.classList.add('d-none');
      }
    });

    this.startsiteService.selectedVideo$.subscribe(video => {
      this.selectedVideo = video;
    });
  }

  subscribeToVideoService() {
    this.videoService.videos$.subscribe(videos => {
      this.videos = videos;
    });
  }

  playVideo(videoElement: HTMLVideoElement) {
    videoElement.play();
  }

  pauseVideo(videoElement: HTMLVideoElement) {
    videoElement.pause();
  }

  togglePlayPause(videoElement: HTMLVideoElement) {
    if (videoElement.paused) {
      videoElement.play();
    } else {
      videoElement.pause();
    }
  }

  toggleDropdown() {
    this.showDropdown = !this.showDropdown;
  }

  changeQuality(event: any) {
    const quality = event.target.value;
    let videoPlayer = document.getElementById('videoPlayer') as HTMLVideoElement;

    switch (quality) {
      case '480p':
        videoPlayer.src = this.selectedVideo.video_file_480p;
        break;
      case '720p':
        videoPlayer.src = this.selectedVideo.video_file_720p;
        break;
      case '1080p':
        videoPlayer.src = this.selectedVideo.video_file_1080p;
        break;
    }

    videoPlayer.load();
    videoPlayer.play();
  }



  selectVideo(video: any) {
    this.startsiteService.selectVideo(video);
    if (video) {
      this.startsiteService.toggleAllVideos(false);
      let videoQualitySelect = document.getElementById('videoQuality') as HTMLSelectElement;
      videoQualitySelect.value = '480p';
    }
  }


  getDaysSinceCreation(created_at: string): string {
    const creationDate = new Date(created_at);
    const currentDate = new Date();

    const diffInMilliseconds = currentDate.getTime() - creationDate.getTime();
    const diffInDays = Math.floor(diffInMilliseconds / (1000 * 60 * 60 * 24));

    return diffInDays === 1 ? diffInDays + ' day ago' : diffInDays + ' days ago';
  }

  onSearchInputChange(event: any) {
    this.searchTerm = event.target.value.toLowerCase();
  }


  getFilteredVideos() {
    return this.searchTerm ?
      this.videos.filter(video => video.title.toLowerCase().includes(this.searchTerm)) :
      this.videos;
  }
}
