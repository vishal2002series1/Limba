import { Component, Input } from '@angular/core';
import { Client } from 'src/app/constants/model';

@Component({
  selector: 'app-client-data',
  templateUrl: './client-data.component.html',
  styleUrls: ['./client-data.component.scss']
})
export class ClientDataComponent {
  @Input() client!: Client;
}
