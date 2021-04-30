import { Controller, Get, Param, Res } from '@nestjs/common';
import { LayoutService } from './layout.service';

@Controller('layout')
export class LayoutController {
    
    constructor(
        private layoutProvider: LayoutService,
    ){
    }

    @Get(':manyty_id')
    getMAnytyDetailsLayout(@Param("manyty_id") mAnytyId, @Res() response) {
        response.setHeader("Content-Type", "application/json");

        
    }
}
