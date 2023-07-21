import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { StartsiteComponent } from './components/startsite/startsite.component';
import { ImprintPpComponent } from './components/imprint-pp/imprint-pp.component';
import { NewVideoComponent } from './components/new-video/new-video.component';
import { ResetpasswordComponent } from './components/resetpassword/resetpassword.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {path: 'login', component: LoginComponent},
  {path: 'startsite', component: StartsiteComponent},
  {path: 'imprint-privacypolicy', component: ImprintPpComponent},
  {path: 'videos', component: NewVideoComponent},
  {path: 'resetpassword/:uid/:token', component: ResetpasswordComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
