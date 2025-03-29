import React from 'react';
import {FilterSidebar} from "../../../components/filters";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {createComponentPages} from "../../../utils/componentFactory";

const {ListPage, DetailPage} = createComponentPages({
    type: 'receivers',
    title: 'Receivers',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="receivers"/>
});

export const ReceiverListPage = ListPage;
export const ReceiverDetailPage = DetailPage;