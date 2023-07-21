import { Component, ViewChild, ElementRef, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';

@Component({
  selector: 'app-resetpassword',
  templateUrl: './resetpassword.component.html',
  styleUrls: ['./resetpassword.component.scss']
})
export class ResetpasswordComponent implements OnInit {
  uid!: string | null;
  token!: string | null;
  passwordOne: string = "";
  passwordTwo: string = "";

  passwordResetted: boolean = false;

  @ViewChild('fmpErrorMessage', { static: false }) fmpErrorMessage!: ElementRef;

  constructor(private route: ActivatedRoute, private router: Router) { }

  ngOnInit(): void {
    this.uid = this.route.snapshot.paramMap.get('uid') ?? '';
    this.token = this.route.snapshot.paramMap.get('token') ?? '';
  }

  async resetPassword(){
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      "uid": this.uid,
      "token": this.token,
      "password1": this.passwordOne,
      "password2": this.passwordTwo
    });

    const requestOptions : RequestInit = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
};

const resp = await fetch("https://googlec-videoflix.niels-scholz.com/authentication/api/reset/password/confirm", requestOptions);

    if (resp.ok) {
       this.passwordResetted = true;
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 1500);
  } else {
      const errorData = await resp.json();
      this.fmpErrorMessage.nativeElement.textContent = errorData.detail;
}
}
}
