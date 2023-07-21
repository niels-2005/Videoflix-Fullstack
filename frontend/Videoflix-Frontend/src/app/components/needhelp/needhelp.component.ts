import { Component, ElementRef, ViewChild } from '@angular/core';

@Component({
  selector: 'app-needhelp',
  templateUrl: './needhelp.component.html',
  styleUrls: ['./needhelp.component.scss']
})
export class NeedhelpComponent {

  email: string = "";

  @ViewChild('fmpErrorMessage', { static: false }) fmpErrorMessage!: ElementRef;

  isButtonDisabled = false;

  emailSended = false;

  async sendResetMail(){
    const myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    const raw = JSON.stringify({
      "email": this.email
    });

    const requestOptions : RequestInit= {
      method: 'POST',
      headers: myHeaders,
      body: raw,
};

const resp = await fetch("https://googlec-videoflix.niels-scholz.com/authentication/api/reset/password/", requestOptions);

this.isButtonDisabled = true;

if (resp.ok) {
  this.emailSended = true;
  this.fmpErrorMessage.nativeElement.textContent = "";
} else {
  const errorData = await resp.json();
  this.fmpErrorMessage.nativeElement.textContent = errorData.detail;
  this.isButtonDisabled = false;
}
}

}
