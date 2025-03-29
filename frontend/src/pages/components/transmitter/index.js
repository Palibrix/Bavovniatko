import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";

const {ListPage, DetailPage} = createComponentPages({
    type: 'transmitters',
    title: 'Video Transmitters',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="transmitters"/>
});

export const TransmitterListPage = ListPage;
export const TransmitterDetailPage = DetailPage;