import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor(private router: Router) {}

  private messageSubject = new Subject<string>();
  message$ = this.messageSubject.asObservable();

  setMessage(message: string) {
    this.messageSubject.next(message);
  }

  checkToken(){
    const token = localStorage.getItem('token');
    if (!token) {
      this.router.navigate(['/login']);
    }
  }

}
