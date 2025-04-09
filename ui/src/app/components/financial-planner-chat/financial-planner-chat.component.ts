import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Client } from 'src/app/constants/model';

@Component({
  selector: 'app-financial-planner-chat',
  templateUrl: './financial-planner-chat.component.html',
  styleUrls: ['./financial-planner-chat.component.scss']
})
export class FinancialPlannerChatComponent implements OnInit {

  clients: Client[] = [];
  selectedClient: Client | undefined;
  siderWidth: string = '55vw'
  isCollapsed = false;

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) {}

  ngOnInit() {
    this.http.get<Client[]>('/assets/metadata/financial_planner_user_profile.json').subscribe(data => {
      this.clients = data;
      if (this.clients.length > 0) {
        this.selectedClient = this.clients[0];
      }
    });
  }

  onSelectClient(client: Client) {
    this.selectedClient = client;
  }

  toggleCollapsed(): void {
    this.isCollapsed = !this.isCollapsed;
    this.cdr.detectChanges(); 
  }
}

