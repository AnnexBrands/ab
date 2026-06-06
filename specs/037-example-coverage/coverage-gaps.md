# Coverage Gaps — 037-example-coverage (T009)

Generated from the precise example index. Two kinds of gap:
- **legacy** = backed only by a deprecated `_`-prefixed runner example → MIGRATE (US4)
- **none** = no example calls it at all → AUTHOR (US1)

Totals: 209 routed, 193 uncovered (132 legacy-only, 61 no-example).

## api.address  (migrate 2, author 0)

- [ ] MIGRATE api.address.get_property_type  (GET → int)  from examples/_address.py
- [ ] MIGRATE api.address.validate  (GET → AddressIsValidResult)  from examples/_address.py

## api.autoprice  (migrate 2, author 0)

- [ ] MIGRATE api.autoprice.quick_quote  (POST → QuickQuoteResponse)  from examples/_autoprice.py
- [ ] MIGRATE api.autoprice.quote_request  (POST → QuoteRequestResponse)  from examples/_autoprice.py

## api.catalog  (migrate 5, author 0)

- [ ] MIGRATE api.catalog.bulk_insert  (POST → )  from examples/_catalog.py
- [ ] MIGRATE api.catalog.create  (POST → CatalogWithSellersDto)  from examples/_catalog.py
- [ ] MIGRATE api.catalog.delete  (DELETE → )  from examples/_catalog.py
- [ ] MIGRATE api.catalog.get  (GET → CatalogExpandedDto)  from examples/_catalog.py
- [ ] MIGRATE api.catalog.update  (PUT → CatalogWithSellersDto)  from examples/_catalog.py

## api.commodities  (migrate 5, author 0)

- [ ] MIGRATE api.commodities.create  (POST → Commodity)  from examples/_commodities.py
- [ ] MIGRATE api.commodities.get  (GET → Commodity)  from examples/_commodities.py
- [ ] MIGRATE api.commodities.search  (POST → List[Commodity])  from examples/_commodities.py
- [ ] MIGRATE api.commodities.suggestions  (POST → List[Commodity])  from examples/_commodities.py
- [ ] MIGRATE api.commodities.update  (PUT → Commodity)  from examples/_commodities.py

## api.commodity_maps  (migrate 5, author 0)

- [ ] MIGRATE api.commodity_maps.create  (POST → CommodityMap)  from examples/_commodities.py
- [ ] MIGRATE api.commodity_maps.delete  (DELETE → ServiceBaseResponse)  from examples/_commodities.py
- [ ] MIGRATE api.commodity_maps.get  (GET → CommodityMap)  from examples/_commodities.py
- [ ] MIGRATE api.commodity_maps.search  (POST → List[CommodityMap])  from examples/_commodities.py
- [ ] MIGRATE api.commodity_maps.update  (PUT → CommodityMap)  from examples/_commodities.py

## api.companies  (migrate 24, author 0)

- [ ] MIGRATE api.companies.available_by_current_user  (GET → List[CompanySimple])  from examples/_companies.py
- [ ] MIGRATE api.companies.create  (POST → str)  from examples/_companies.py
- [ ] MIGRATE api.companies.get_brands  (GET → List[CompanyBrand])  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_brands_tree  (GET → List[BrandTree])  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_by_id  (GET → CompanySimple)  from examples/_companies.py
- [ ] MIGRATE api.companies.get_carrier_accounts  (GET → List[CarrierAccount])  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_details  (GET → CompanyDetails)  from examples/_companies.py
- [ ] MIGRATE api.companies.get_fulldetails  (GET → CompanyDetails)  from examples/_companies.py
- [ ] MIGRATE api.companies.get_geo_area_companies  (GET → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_geo_settings  (GET → GeoSettings)  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_global_geo_settings  (GET → GeoSettings)  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_inherited_packaging_labor  (GET → PackagingLabor)  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_inherited_packaging_tariffs  (GET → List[PackagingTariff])  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_packaging_labor  (GET → PackagingLabor)  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.get_packaging_settings  (GET → PackagingSettings)  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.list  (POST → List[CompanySimple])  from examples/_companies.py
- [ ] MIGRATE api.companies.save_carrier_accounts  (POST → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.save_geo_settings  (POST → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.save_packaging_labor  (POST → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.save_packaging_settings  (POST → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.search  (POST → List[SearchCompanyResponse])  from examples/_companies.py
- [ ] MIGRATE api.companies.search_carrier_accounts  (GET → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.suggest_carriers  (GET → )  from examples/_companies_extended.py
- [ ] MIGRATE api.companies.update_fulldetails  (PUT → CompanyDetails)  from examples/_companies.py

## api.contacts  (migrate 12, author 0)

- [ ] MIGRATE api.contacts.create  (POST → )  from examples/_contacts.py
- [ ] MIGRATE api.contacts.get  (GET → ContactSimple)  from examples/_contacts.py
- [ ] MIGRATE api.contacts.get_current_user  (GET → ContactSimple)  from examples/_contacts.py
- [ ] MIGRATE api.contacts.get_details  (GET → ContactDetailedInfo)  from examples/_contacts.py
- [ ] MIGRATE api.contacts.get_history_aggregated  (GET → ContactHistoryAggregated)  from examples/_contacts_extended.py
- [ ] MIGRATE api.contacts.get_history_graph_data  (GET → ContactGraphData)  from examples/_contacts_extended.py
- [ ] MIGRATE api.contacts.get_primary_details  (GET → ContactPrimaryDetails)  from examples/_contacts.py
- [ ] MIGRATE api.contacts.merge  (PUT → )  from examples/_contacts_extended.py
- [ ] MIGRATE api.contacts.merge_preview  (POST → ContactMergePreview)  from examples/_contacts_extended.py
- [ ] MIGRATE api.contacts.post_history  (POST → ContactHistory)  from examples/_contacts_extended.py
- [ ] MIGRATE api.contacts.search  (POST → List[SearchContactEntityResult])  from examples/_contacts.py
- [ ] MIGRATE api.contacts.update_details  (PUT → )  from examples/_contacts.py

## api.dashboard  (migrate 0, author 7)

- [ ] AUTHOR  api.dashboard.get_grid_view_state  (GET → GridViewState)
- [ ] AUTHOR  api.dashboard.in_house  (POST → )
- [ ] AUTHOR  api.dashboard.inbound  (POST → )
- [ ] AUTHOR  api.dashboard.local_deliveries  (POST → )
- [ ] AUTHOR  api.dashboard.outbound  (POST → )
- [ ] AUTHOR  api.dashboard.recent_estimates  (POST → )
- [ ] AUTHOR  api.dashboard.save_grid_view_state  (POST → )

## api.documents  (migrate 3, author 0)

- [ ] MIGRATE api.documents.list  (GET → List[Document])  from examples/_documents.py
- [ ] MIGRATE api.documents.update  (PUT → )  from examples/_documents.py
- [ ] MIGRATE api.documents.upload  (POST → DocumentUploadResponse)  from examples/_documents.py

## api.jobs  (migrate 14, author 1)

- [ ] AUTHOR  api.jobs.transfer  (POST → )
- [ ] MIGRATE api.jobs.add_freight_items  (POST → )  from examples/_freight_providers.py
- [ ] MIGRATE api.jobs.add_item_notes  (POST → ServiceBaseResponse)  from examples/_jobs.py
- [ ] MIGRATE api.jobs.change_agent  (POST → ServiceBaseResponse)  from examples/_agent.py
- [ ] MIGRATE api.jobs.create  (POST → )  from examples/_jobs.py
- [ ] MIGRATE api.jobs.get  (GET → Job)  from examples/_jobs.py
- [ ] MIGRATE api.jobs.get_calendar_items  (GET → List[CalendarItem])  from examples/_jobs.py
- [ ] MIGRATE api.jobs.get_packaging_containers  (GET → List[PackagingContainer])  from examples/_jobs.py
- [ ] MIGRATE api.jobs.get_price  (GET → JobPrice)  from examples/_jobs.py
- [ ] MIGRATE api.jobs.get_update_page_config  (GET → JobUpdatePageConfig)  from examples/_jobs.py
- [ ] MIGRATE api.jobs.save  (PUT → )  from examples/_jobs.py
- [ ] MIGRATE api.jobs.search  (GET → JobSearchResult)  from examples/_jobs.py
- [ ] MIGRATE api.jobs.search_by_details  (POST → List[JobSearchResult])  from examples/_jobs.py
- [ ] MIGRATE api.jobs.update  (POST → )  from examples/_jobs.py
- [ ] MIGRATE api.jobs.update_item  (PUT → ServiceBaseResponse)  from examples/_jobs.py

## api.jobs.email  (migrate 0, author 3)

- [ ] AUTHOR  api.jobs.email.create_transactional  (POST → )
- [ ] AUTHOR  api.jobs.email.send_document  (POST → )
- [ ] AUTHOR  api.jobs.email.send_template  (POST → )

## api.jobs.form  (migrate 0, author 1)

- [ ] AUTHOR  api.jobs.form.shipments  (GET → List[FormsShipmentPlan])

## api.jobs.freight_providers  (migrate 0, author 3)

- [ ] AUTHOR  api.jobs.freight_providers.list  (GET → List[PricedFreightProvider])
- [ ] AUTHOR  api.jobs.freight_providers.rate_quote  (POST → )
- [ ] AUTHOR  api.jobs.freight_providers.save  (POST → )

## api.jobs.note  (migrate 0, author 4)

- [ ] AUTHOR  api.jobs.note.create  (POST → JobNote)
- [ ] AUTHOR  api.jobs.note.get  (GET → JobNote)
- [ ] AUTHOR  api.jobs.note.list  (GET → List[JobNote])
- [ ] AUTHOR  api.jobs.note.update  (PUT → JobNote)

## api.jobs.on_hold  (migrate 0, author 6)

- [ ] AUTHOR  api.jobs.on_hold.add_comment  (POST → OnHoldNoteDetails)
- [ ] AUTHOR  api.jobs.on_hold.delete  (DELETE → )
- [ ] AUTHOR  api.jobs.on_hold.get  (GET → OnHoldDetails)
- [ ] AUTHOR  api.jobs.on_hold.list_followup_users  (GET → List[OnHoldUser])
- [ ] AUTHOR  api.jobs.on_hold.update  (PUT → SaveOnHoldResponse)
- [ ] AUTHOR  api.jobs.on_hold.update_dates  (PUT → )

## api.jobs.parcel_items  (migrate 0, author 4)

- [ ] AUTHOR  api.jobs.parcel_items.create  (POST → ParcelItem)
- [ ] AUTHOR  api.jobs.parcel_items.delete  (DELETE → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.parcel_items.list  (GET → List[ParcelItem])
- [ ] AUTHOR  api.jobs.parcel_items.list_with_materials  (GET → List[ParcelItemWithMaterials])

## api.jobs.payment  (migrate 0, author 10)

- [ ] AUTHOR  api.jobs.payment.ach_credit_transfer  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.payment.attach_customer_bank  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.payment.cancel_ach_verification  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.payment.create_ach_session  (POST → ACHSessionResponse)
- [ ] AUTHOR  api.jobs.payment.get  (GET → PaymentInfo)
- [ ] AUTHOR  api.jobs.payment.get_create  (GET → PaymentInfo)
- [ ] AUTHOR  api.jobs.payment.get_sources  (GET → List[PaymentSource])
- [ ] AUTHOR  api.jobs.payment.pay_by_source  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.payment.set_bank_source  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.payment.verify_ach_source  (POST → ServiceBaseResponse)

## api.jobs.rfq  (migrate 0, author 2)

- [ ] AUTHOR  api.jobs.rfq.list  (GET → List[QuoteRequestDisplayInfo])
- [ ] AUTHOR  api.jobs.rfq.status  (GET → int)

## api.jobs.shipment  (migrate 0, author 11)

- [ ] AUTHOR  api.jobs.shipment.add_accessorial  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.shipment.book  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.shipment.delete  (DELETE → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.shipment.get_accessorials  (GET → List[Accessorial])
- [ ] AUTHOR  api.jobs.shipment.get_export_data  (GET → ShipmentExportData)
- [ ] AUTHOR  api.jobs.shipment.get_origin_destination  (GET → ShipmentOriginDestination)
- [ ] AUTHOR  api.jobs.shipment.get_rate_quotes  (GET → List[RateQuote])
- [ ] AUTHOR  api.jobs.shipment.get_rates_state  (GET → RatesState)
- [ ] AUTHOR  api.jobs.shipment.post_export_data  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.shipment.remove_accessorial  (DELETE → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.shipment.request_rate_quotes  (POST → List[RateQuote])

## api.jobs.sms  (migrate 0, author 4)

- [ ] AUTHOR  api.jobs.sms.get_template  (GET → )
- [ ] AUTHOR  api.jobs.sms.list  (GET → )
- [ ] AUTHOR  api.jobs.sms.mark_read  (POST → )
- [ ] AUTHOR  api.jobs.sms.send  (POST → )

## api.jobs.status  (migrate 0, author 1)

- [ ] AUTHOR  api.jobs.status.set_quote  (POST → ServiceBaseResponse)

## api.jobs.timeline  (migrate 0, author 2)

- [ ] AUTHOR  api.jobs.timeline.increment_status  (POST → ServiceBaseResponse)
- [ ] AUTHOR  api.jobs.timeline.undo_increment_status  (POST → ServiceBaseResponse)

## api.jobs.tracking  (migrate 0, author 2)

- [ ] AUTHOR  api.jobs.tracking.get  (GET → TrackingInfo)
- [ ] AUTHOR  api.jobs.tracking.v3  (GET → TrackingInfoV3)

## api.lookup  (migrate 14, author 0)

- [ ] MIGRATE api.lookup.get_access_key  (GET → AccessKeySetup)  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_access_keys  (GET → List[AccessKey])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_by_key_and_id  (GET → LookupValue)  from examples/_lookup_extended.py
- [ ] MIGRATE api.lookup.get_common_insurance  (GET → List[CommonInsuranceSlab])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_contact_types  (GET → List[ContactTypeEntity])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_countries  (GET → List[CountryCodeDto])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_density_class_map  (GET → List[DensityClassEntry])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_document_types  (GET → List[DocumentTypeBySource])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_items  (GET → List[LookupItem])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_job_statuses  (GET → List[JobStatus])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_parcel_package_types  (GET → List[ParcelPackageType])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_ppc_campaigns  (GET → List[PPCCampaign])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.get_refer_category_hierarchy  (GET → List[LookupValue])  from examples/_lookup.py
- [ ] MIGRATE api.lookup.reset_cache  (GET → )  from examples/_lookup_extended.py

## api.lots  (migrate 5, author 0)

- [ ] MIGRATE api.lots.create  (POST → LotDto)  from examples/_lots.py
- [ ] MIGRATE api.lots.delete  (DELETE → )  from examples/_lots.py
- [ ] MIGRATE api.lots.get  (GET → LotDto)  from examples/_lots.py
- [ ] MIGRATE api.lots.get_overrides  (POST → List[LotOverrideDto])  from examples/_lots.py
- [ ] MIGRATE api.lots.update  (PUT → LotDto)  from examples/_lots.py

## api.notes  (migrate 2, author 0)

- [ ] MIGRATE api.notes.create  (POST → GlobalNote)  from examples/_notes_global.py
- [ ] MIGRATE api.notes.update  (PUT → GlobalNote)  from examples/_notes_global.py

## api.partners  (migrate 3, author 0)

- [ ] MIGRATE api.partners.get  (GET → Partner)  from examples/_partners.py
- [ ] MIGRATE api.partners.list  (GET → List[Partner])  from examples/_partners.py
- [ ] MIGRATE api.partners.search  (POST → List[Partner])  from examples/_partners.py

## api.reports  (migrate 8, author 0)

- [ ] MIGRATE api.reports.insurance  (POST → List[InsuranceReport])  from examples/_reports.py
- [ ] MIGRATE api.reports.referred_by  (POST → List[ReferredByReport])  from examples/_reports.py
- [ ] MIGRATE api.reports.sales  (POST → List[SalesForecastReport])  from examples/_reports.py
- [ ] MIGRATE api.reports.sales_drilldown  (POST → List[RevenueCustomer])  from examples/_reports.py
- [ ] MIGRATE api.reports.sales_summary  (POST → SalesForecastSummary)  from examples/_reports.py
- [ ] MIGRATE api.reports.top_revenue_customers  (POST → List[RevenueCustomer])  from examples/_reports.py
- [ ] MIGRATE api.reports.top_revenue_sales_reps  (POST → List[RevenueCustomer])  from examples/_reports.py
- [ ] MIGRATE api.reports.web2lead  (POST → List[Web2LeadReport])  from examples/_reports.py

## api.rfq  (migrate 7, author 0)

- [ ] MIGRATE api.rfq.accept  (POST → )  from examples/_rfq.py
- [ ] MIGRATE api.rfq.accept_winner  (POST → )  from examples/_rfq.py
- [ ] MIGRATE api.rfq.add_comment  (POST → )  from examples/_rfq.py
- [ ] MIGRATE api.rfq.cancel  (POST → )  from examples/_rfq.py
- [ ] MIGRATE api.rfq.decline  (POST → )  from examples/_rfq.py
- [ ] MIGRATE api.rfq.get  (GET → QuoteRequestDisplayInfo)  from examples/_rfq.py
- [ ] MIGRATE api.rfq.get_for_job  (GET → List[QuoteRequestDisplayInfo])  from examples/_rfq.py

## api.sellers  (migrate 4, author 0)

- [ ] MIGRATE api.sellers.create  (POST → SellerDto)  from examples/_sellers.py
- [ ] MIGRATE api.sellers.delete  (DELETE → )  from examples/_sellers.py
- [ ] MIGRATE api.sellers.get  (GET → SellerExpandedDto)  from examples/_sellers.py
- [ ] MIGRATE api.sellers.update  (PUT → SellerDto)  from examples/_sellers.py

## api.shipments  (migrate 3, author 0)

- [ ] MIGRATE api.shipments.get_global_accessorials  (GET → List[GlobalAccessorial])  from examples/_shipments.py
- [ ] MIGRATE api.shipments.get_shipment  (GET → ShipmentInfo)  from examples/_shipments.py
- [ ] MIGRATE api.shipments.get_shipment_document  (GET → bytes)  from examples/_shipments.py

## api.users  (migrate 4, author 0)

- [ ] MIGRATE api.users.create  (POST → )  from examples/_users.py
- [ ] MIGRATE api.users.get_roles  (GET → List[str])  from examples/_users.py
- [ ] MIGRATE api.users.list  (POST → List[User])  from examples/_users.py
- [ ] MIGRATE api.users.update  (PUT → )  from examples/_users.py

## api.views  (migrate 8, author 0)

- [ ] MIGRATE api.views.create  (POST → GridViewDetails)  from examples/_views.py
- [ ] MIGRATE api.views.delete  (DELETE → ServiceBaseResponse)  from examples/_views.py
- [ ] MIGRATE api.views.get  (GET → GridViewDetails)  from examples/_views.py
- [ ] MIGRATE api.views.get_access_info  (GET → GridViewAccess)  from examples/_views.py
- [ ] MIGRATE api.views.get_dataset_sp  (GET → List[StoredProcedureColumn])  from examples/_views.py
- [ ] MIGRATE api.views.get_dataset_sps  (GET → List[StoredProcedureColumn])  from examples/_views.py
- [ ] MIGRATE api.views.list  (GET → List[GridViewDetails])  from examples/_views.py
- [ ] MIGRATE api.views.update_access  (PUT → )  from examples/_views.py

## api.web2lead  (migrate 2, author 0)

- [ ] MIGRATE api.web2lead.get  (GET → Web2LeadResponse)  from examples/_web2lead.py
- [ ] MIGRATE api.web2lead.post  (POST → Web2LeadResponse)  from examples/_web2lead.py

