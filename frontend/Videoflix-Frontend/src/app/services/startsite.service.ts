import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StartsiteService {

  constructor() { }

  private _showAllVideos = new BehaviorSubject<boolean>(true);
  showAllVideos$ = this._showAllVideos.asObservable();

  private _selectedVideo = new BehaviorSubject<any>(null);
  selectedVideo$ = this._selectedVideo.asObservable();

  private _videos = new BehaviorSubject<any[]>([]);
  videos$ = this._videos.asObservable();


  toggleAllVideos(show: boolean) {
    this._showAllVideos.next(show);
  }

  selectVideo(video: any) {
    this._selectedVideo.next(video);
  }

  updateVideos(videos: any[]) {
    this._videos.next(videos);
  }

  filterVideos(searchTerm: string) {
    let currentVideos = this._videos.value;
    let filteredVideos = currentVideos.filter(video =>
      video.title.toLowerCase().includes(searchTerm.toLowerCase())
    );
    this._videos.next(filteredVideos);
  }
}
