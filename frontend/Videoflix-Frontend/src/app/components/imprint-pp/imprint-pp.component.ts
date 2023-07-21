import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from 'src/app/services/authentication.service';

@Component({
  selector: 'app-imprint-pp',
  templateUrl: './imprint-pp.component.html',
  styleUrls: ['./imprint-pp.component.scss']
})
export class ImprintPpComponent implements OnInit {

  constructor(private tokenService: AuthenticationService) {}

  ngOnInit(): void {
      this.tokenService.checkToken();
  }

}
