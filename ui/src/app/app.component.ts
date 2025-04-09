import { Component } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})

export class AppComponent {
  isTestedUI = false;

  constructor(private router: Router){
    this.router.events.subscribe(
      (event:any)=>{
        if(event instanceof NavigationEnd){
          if(event.url === '/user-chat'){
            this.isTestedUI = true;
          }
        }
      }
    )
  }

}
