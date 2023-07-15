import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  private messageSubject = new Subject<string>();
  message$ = this.messageSubject.asObservable();

  setMessage(message: string) {
    this.messageSubject.next(message);
  }
}
