import { Component } from '@angular/core';

@Component({
  selector: 'app-irah-for-esg',
  templateUrl: './irah-for-esg.component.html',
  styleUrl: './irah-for-esg.component.scss'
})
export class IrahForEsgComponent {

  ngOnInit(): void {
    window.location.href = 'https://ue2dfas09zwap01.azurewebsites.net';
  }
  
}
