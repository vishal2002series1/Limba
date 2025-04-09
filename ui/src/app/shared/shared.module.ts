import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader/loader.component';
import { HeaderComponent } from './header/header.component';
import { UserChatService } from './services/user-chat.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BotResponseComponent } from './bot-response/bot-response.component';
import { TooltipModule } from 'ngx-bootstrap/tooltip';
import { TabsModule } from 'ngx-bootstrap/tabs';
import { CommonChatComponent } from './common-chat/common-chat.component';
import { MarkdownModule } from 'ngx-markdown';
import { NzBreadCrumbModule } from 'ng-zorro-antd/breadcrumb';
import { NzButtonModule } from 'ng-zorro-antd/button';
import { NzAlertModule } from 'ng-zorro-antd/alert';
import { NzCollapseModule } from 'ng-zorro-antd/collapse';
import { NzCheckboxModule } from 'ng-zorro-antd/checkbox';
import { NzDropDownModule } from 'ng-zorro-antd/dropdown';
import { NzGridModule } from 'ng-zorro-antd/grid';
import { NzI18nModule } from 'ng-zorro-antd/i18n';
import { NzIconModule } from 'ng-zorro-antd/icon';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzInputNumberModule } from 'ng-zorro-antd/input-number';
import { NzPopoverModule } from 'ng-zorro-antd/popover';
import { NzSpinModule } from 'ng-zorro-antd/spin';
import { NzSelectModule } from 'ng-zorro-antd/select';
import { NzSwitchModule } from 'ng-zorro-antd/switch';
import { NzUploadModule } from 'ng-zorro-antd/upload';
import { NzTreeSelectModule } from 'ng-zorro-antd/tree-select';
import { NzLayoutModule } from 'ng-zorro-antd/layout';
import { NzListModule } from 'ng-zorro-antd/list';
import { NzModalModule } from 'ng-zorro-antd/modal';
import { NzTabsModule } from 'ng-zorro-antd/tabs';
import { NzTagModule } from 'ng-zorro-antd/tag';
import { NzRadioModule } from 'ng-zorro-antd/radio';
import { NzMenuModule } from 'ng-zorro-antd/menu';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzPopconfirmModule } from 'ng-zorro-antd/popconfirm';
import { NzResultModule } from 'ng-zorro-antd/result';
import { NzTypographyModule } from 'ng-zorro-antd/typography';
import { NzFlexModule } from 'ng-zorro-antd/flex';
import { NzAffixModule } from 'ng-zorro-antd/affix';
import { NzBackTopModule } from 'ng-zorro-antd/back-top';
import { NzDividerModule } from 'ng-zorro-antd/divider';
import { IconDefinition } from '@ant-design/icons-angular';
import {
  HistoryOutline, EditOutline, DeleteOutline, DashOutline,
  LikeOutline,
  DislikeFill,
  LikeFill,
  DislikeOutline,
  EyeOutline,
  MenuFoldOutline,
  MenuUnfoldOutline,
  CloseOutline,
  HomeOutline
} from '@ant-design/icons-angular/icons';
import { NzToolTipModule } from 'ng-zorro-antd/tooltip';
import { SidebarComponent } from './sidebar/sidebar.component';
import { ChartsComponent } from './charts/charts.component';
import { ClientDataComponent } from './client-data/client-data.component';
import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';
import { AppRoutingModule } from '../app-routing.module';
import { FinancialChatComponent } from './financial-chat/financial-chat.component';
import { FinancialResponseComponent } from './financial-response/financial-response.component';

PlotlyModule.plotlyjs = PlotlyJS;
const icons: IconDefinition[] = 
[ 
  HistoryOutline, 
  EditOutline, 
  DeleteOutline, 
  DashOutline, 
  LikeOutline, 
  LikeFill, 
  DislikeOutline, 
  DislikeFill, 
  EyeOutline, 
  MenuFoldOutline, 
  MenuUnfoldOutline,
  CloseOutline,
  HomeOutline 
];

@NgModule({
  declarations: [
    LoaderComponent,
    HeaderComponent,
    BotResponseComponent,
    CommonChatComponent,
    FinancialChatComponent,
    ChartsComponent,
    ClientDataComponent,
    SidebarComponent,
    FinancialResponseComponent
  ],
  imports: [
    CommonModule,
    HttpClientModule,
    ReactiveFormsModule,
    AppRoutingModule,
    TooltipModule.forRoot(),
    FormsModule,
    TabsModule.forRoot(),
    MarkdownModule.forRoot(),
    NzIconModule.forChild(icons),
    NzModalModule,
    NzButtonModule,
    NzAlertModule,
    NzButtonModule,
    NzBreadCrumbModule,
    NzCheckboxModule,
    NzCollapseModule,
    NzDropDownModule,
    NzGridModule,
    NzI18nModule,
    NzRadioModule,
    NzIconModule,
    NzInputModule,
    NzInputNumberModule,
    NzMenuModule,
    NzModalModule,
    NzLayoutModule,
    NzListModule,
    NzPopoverModule,
    NzSelectModule,
    NzSpinModule,
    NzSwitchModule,
    NzTreeSelectModule,
    NzTabsModule,
    NzTagModule,
    NzFormModule,
    NzUploadModule,
    NzPopconfirmModule,
    NzResultModule,
    NzTypographyModule,
    NzPopoverModule,
    NzPopconfirmModule,
    NzFlexModule,
    NzAffixModule,
    NzToolTipModule,
    NzBackTopModule,
    NzDividerModule,    
    PlotlyModule
  ],
  exports: [
    LoaderComponent,
    HeaderComponent,
    BotResponseComponent,
    CommonChatComponent,
    FinancialChatComponent,
    ChartsComponent,
    ClientDataComponent,
    SidebarComponent,
    NzAlertModule,
    NzButtonModule,
    NzBreadCrumbModule,
    NzCheckboxModule,
    NzCollapseModule,
    NzDropDownModule,
    NzGridModule,
    NzI18nModule,
    NzRadioModule,
    NzIconModule,
    NzInputModule,
    NzInputNumberModule,
    NzMenuModule,
    NzModalModule,
    NzLayoutModule,
    NzListModule,
    NzPopoverModule,
    NzSelectModule,
    NzSpinModule,
    NzSwitchModule,
    NzTreeSelectModule,
    NzTabsModule,
    NzTagModule,
    NzFormModule,
    NzUploadModule,
    NzPopconfirmModule,
    NzResultModule,
    NzTypographyModule,
    NzPopoverModule,
    NzPopconfirmModule,
    NzFlexModule,
    NzAffixModule,
    NzToolTipModule,
    NzBackTopModule,
    NzDividerModule,    
    PlotlyModule
  ],
  providers: [UserChatService]
})
export class SharedModule { }
