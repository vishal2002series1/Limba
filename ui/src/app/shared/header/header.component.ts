import { Component, Input, OnInit } from '@angular/core';
import { UserChatService } from '../services/user-chat.service';
import { map, of, take } from 'rxjs';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})

export class HeaderComponent implements OnInit {
  
  $loggedUser = this.userChat.getProfile().pipe(map((user) => user.map((user) => user.user_id)));
  @Input() isTestedUI : boolean | undefined; 
  constructor(private userChat: UserChatService) { }

  ngOnInit(): void {
    this.$loggedUser.pipe(take(1)).subscribe(res => this.userChat.getUser(res[0]));
  }

}
