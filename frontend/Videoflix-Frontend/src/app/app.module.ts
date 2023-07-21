import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { SignupComponent } from './components/signup/signup.component';
import { NeedhelpComponent } from './components/needhelp/needhelp.component';
import { StartsiteComponent } from './components/startsite/startsite.component';
import { HeaderbarComponent } from './components/headerbar/headerbar.component';
import { ImprintPpComponent } from './components/imprint-pp/imprint-pp.component';
import { NewVideoComponent } from './components/new-video/new-video.component';
import { ResetpasswordComponent } from './components/resetpassword/resetpassword.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SignupComponent,
    NeedhelpComponent,
    StartsiteComponent,
    HeaderbarComponent,
    ImprintPpComponent,
    NewVideoComponent,
    ResetpasswordComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
