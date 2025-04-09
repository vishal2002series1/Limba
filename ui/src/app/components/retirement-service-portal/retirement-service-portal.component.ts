import { Component } from '@angular/core';

@Component({
  selector: 'app-retirement-service-portal',
  templateUrl: './retirement-service-portal.component.html',
  styleUrl: './retirement-service-portal.component.scss'
})
export class RetirementServicePortalComponent {

  ngOnInit(): void {
    window.location.href = 'https://sda-ey-wamcloud-demo-clientapp.azurewebsites.net/';
  }

}
