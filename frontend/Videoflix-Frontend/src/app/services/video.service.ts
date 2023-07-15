import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VideoService {

  private videos: any[] = [];
  public videos$ = new Subject<any[]>();

  constructor() { }

  async getVideos(){
    const requestOptions : RequestInit = {
      method: 'GET',
    };

    await fetch("https://googlec-videoflix.niels-scholz.com/v1/videos/", requestOptions)
      .then(response => response.json())
      .then(result => {
        this.videos = result;
        this.videos$.next(this.videos);
        console.log(result);
      })
      .catch(error => console.log('error', error));
  }
}
