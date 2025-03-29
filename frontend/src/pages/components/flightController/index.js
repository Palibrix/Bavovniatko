import React from 'react';
import {FilterSidebar} from "../../../components/filters";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {createComponentPages} from "../../../utils/componentFactory";

const {ListPage, DetailPage} = createComponentPages({
    type: 'flight_controllers',
    title: 'Flight Controllers',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="flight_controllers"/>
});

export const FlightControllerListPage = ListPage;
export const FlightControllerDetailPage = DetailPage;