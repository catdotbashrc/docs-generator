Java API Service Documentation Template
=====================================

.. note::
   **Purpose**: Eliminate "shooting in the dark" at API endpoints by documenting Java web services systematically.
   Generated from standardized templates to ensure comprehensive API documentation across all projects.

Project Overview
---------------

:Client: Example Organization
:Service: UtilizationService
:Environment: Production
:Base URL: http://localhost:8080
:Service Type: SOAP Web Service
:Last Updated: 2024-01-01

.. warning::
   **Service Dependencies**: This documentation covers API endpoints and their expected behavior.
   Test all endpoints in non-production environments first.

API Endpoints
------------

SOAP Web Service
~~~~~~~~~~~~~~~

.. list-table:: Service Configuration
   :header-rows: 1
   :widths: 30 70

   * - Property
     - Value
   * - WSDL URL
     - http://localhost:8080/UtilizationService?wsdl
   * - Namespace  
     - http://api.example-client.com/services/
   * - Service Name
     - UtilizationService
   * - Port
     - 8080

Endpoint Reference
~~~~~~~~~~~~~~~~~


**getSupportedTitles**

.. code-block:: xml

   <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:util="http://api.example-client.com/services/">
      <soap:Header/>
      <soap:Body>
         <util:getSupportedTitles>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:workUnit>example_string</util:workUnit>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:category>example_string</util:category>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtCategory>example_string</util:dtCategory>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:title>example_string</util:title>
            
         </util:getSupportedTitles>
      </soap:Body>
   </soap:Envelope>

*Parameters:*

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parameter
     - Type  
     - Description
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - workUnit
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - category
     - String
     - Parameter of type String
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtCategory
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   

*Returns:* SupportedTitleModel

*Purpose:* TODO: Document endpoint purpose


**runSummaryReport**

.. code-block:: xml

   <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:util="http://api.example-client.com/services/">
      <soap:Header/>
      <soap:Body>
         <util:runSummaryReport>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:workUnit>example_string</util:workUnit>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:category>example_string</util:category>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtCategory>example_string</util:dtCategory>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:title>example_string</util:title>
            
         </util:runSummaryReport>
      </soap:Body>
   </soap:Envelope>

*Parameters:*

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parameter
     - Type  
     - Description
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - workUnit
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - category
     - String
     - Parameter of type String
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtCategory
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   

*Returns:* SummaryPage

*Purpose:* TODO: Document endpoint purpose


**runUtilizationReport**

.. code-block:: xml

   <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:util="http://api.example-client.com/services/">
      <soap:Header/>
      <soap:Body>
         <util:runUtilizationReport>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:workUnit>example_string</util:workUnit>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:category>example_string</util:category>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtCategory>example_string</util:dtCategory>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:title>example_string</util:title>
            
         </util:runUtilizationReport>
      </soap:Body>
   </soap:Envelope>

*Parameters:*

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parameter
     - Type  
     - Description
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - workUnit
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - category
     - String
     - Parameter of type String
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtCategory
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   

*Returns:* UtilizationPage

*Purpose:* TODO: Document endpoint purpose


**runUnavailabilityReport**

.. code-block:: xml

   <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
                  xmlns:util="http://api.example-client.com/services/">
      <soap:Header/>
      <soap:Body>
         <util:runUnavailabilityReport>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:workUnit>example_string</util:workUnit>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:category>example_string</util:category>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtCategory>example_string</util:dtCategory>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:startDate>example_string</util:startDate>
            
            <util:endDate>example_string</util:endDate>
            
            <util:title>example_string</util:title>
            
            <util:location>example_string</util:location>
            
            <util:isTotalReport>true</util:isTotalReport>
            
            <util:dtLocation>example_string</util:dtLocation>
            
            <util:dtSubcategory>example_string</util:dtSubcategory>
            
            <util:dtColumnName>example_string</util:dtColumnName>
            
            <util:queryDate>example_string</util:queryDate>
            
            <util:title>example_string</util:title>
            
         </util:runUnavailabilityReport>
      </soap:Body>
   </soap:Envelope>

*Parameters:*

.. list-table::
   :header-rows: 1
   :widths: 25 25 50

   * - Parameter
     - Type  
     - Description
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - workUnit
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - category
     - String
     - Parameter of type String
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtCategory
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - startDate
     - String
     - Parameter of type String
   
   * - endDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   
   * - location
     - String
     - Parameter of type String
   
   * - isTotalReport
     - Boolean
     - Parameter of type Boolean
   
   * - dtLocation
     - String
     - Parameter of type String
   
   * - dtSubcategory
     - String
     - Parameter of type String
   
   * - dtColumnName
     - String
     - Parameter of type String
   
   * - queryDate
     - String
     - Parameter of type String
   
   * - title
     - String
     - Parameter of type String
   

*Returns:* UnavailabilityPage

*Purpose:* TODO: Document endpoint purpose



Data Models
----------


**LocationUtilization**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for LocationUtilization

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - tasks
     - int
     - private field of type int
   
   * - nextDayTasks
     - int
     - private field of type int
   
   * - overtimeTasks
     - int
     - private field of type int
   
   * - overtimeNextDayTasks
     - int
     - private field of type int
   
   * - unavailabilities
     - int
     - private field of type int
   
   * - nextDayUnavailabilities
     - int
     - private field of type int
   
   * - workingNextDay
     - boolean
     - private field of type boolean
   
   * - startedPreviousDay
     - boolean
     - private field of type boolean
   
   * - overtimeHours
     - Integer
     - private field of type Integer
   
   * - overtimeMinutes
     - Integer
     - private field of type Integer
   
   * - detachments
     - List<DetachmentModel>
     - private field of type List<DetachmentModel>
   
   * - attachments
     - List<DetachmentModel>
     - private field of type List<DetachmentModel>
   
   * - totalAttachedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalDetachedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentDetachmentFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentAttachmentFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentInZoneFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentOutOfZoneFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentInZoneFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentOutOfZoneFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - nextDayDetachments
     - List<DetachmentModel>
     - private field of type List<DetachmentModel>
   
   * - nextDayAttachments
     - List<DetachmentModel>
     - private field of type List<DetachmentModel>
   
   * - totalAttachedNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalDetachedNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentDetachmentNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentAttachmentNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentInZoneNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentOutOfZoneNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentInZoneNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentOutOfZoneNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledChartPersonnel
     - Set<Long>
     - private field of type Set<Long>
   
   * - cancelledVacationPersonnel
     - Set<Long>
     - private field of type Set<Long>
   
   * - cancelledChartAndVacationPersonnel
     - Set<Long>
     - private field of type Set<Long>
   
   * - cancelledSundayPersonnel
     - Set<Long>
     - private field of type Set<Long>
   
   * - cancelledHolidayPersonnel
     - Set<Long>
     - private field of type Set<Long>
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledChartAndVacations
     - Integer
     - private field of type Integer
   
   * - cancelledSunday
     - Integer
     - private field of type Integer
   
   * - cancelledHoliday
     - Integer
     - private field of type Integer
   
   * - cancelledChartTasks
     - Integer
     - private field of type Integer
   
   * - cancelledVacationTasks
     - Integer
     - private field of type Integer
   
   * - cancelledChartAndVacationTasks
     - Integer
     - private field of type Integer
   
   * - nextDayCancelledChartTasks
     - Integer
     - private field of type Integer
   
   * - nextDayCancelledVacationTasks
     - Integer
     - private field of type Integer
   
   * - nextDayCancelledChartAndVacationTasks
     - Integer
     - private field of type Integer
   
   * - scheduledCharts
     - Integer
     - private field of type Integer
   
   * - scheduledVacations
     - Integer
     - private field of type Integer
   
   * - scheduledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - sunday
     - Integer
     - private field of type Integer
   
   * - sundayAndVacation
     - Integer
     - private field of type Integer
   
   * - holiday
     - Integer
     - private field of type Integer
   
   * - holidayAndChart
     - Integer
     - private field of type Integer
   
   * - holidayAndVacation
     - Integer
     - private field of type Integer
   
   * - holidayAndVacationAndChart
     - Integer
     - private field of type Integer
   
   * - xwp
     - Integer
     - private field of type Integer
   
   * - nextDayXwp
     - Integer
     - private field of type Integer
   
   * - xwop
     - Integer
     - private field of type Integer
   
   * - nextDayXwop
     - Integer
     - private field of type Integer
   
   * - cvXwp
     - Integer
     - private field of type Integer
   
   * - nextDayCvXwp
     - Integer
     - private field of type Integer
   
   * - cvXwop
     - Integer
     - private field of type Integer
   
   * - nextDayCvXwop
     - Integer
     - private field of type Integer
   
   * - lwopX
     - Integer
     - private field of type Integer
   
   * - nextDayLwopX
     - Integer
     - private field of type Integer
   
   * - paternityLeave
     - Integer
     - private field of type Integer
   
   * - nextDayPaternityLeave
     - Integer
     - private field of type Integer
   
   * - ds95
     - Integer
     - private field of type Integer
   
   * - nextDayDs95
     - Integer
     - private field of type Integer
   
   * - lateness
     - Integer
     - private field of type Integer
   
   * - nextDayLateness
     - Integer
     - private field of type Integer
   
   * - otherExcused
     - Integer
     - private field of type Integer
   
   * - nextDayOtherExcused
     - Integer
     - private field of type Integer
   
   * - sick
     - Integer
     - private field of type Integer
   
   * - nextDaySick
     - Integer
     - private field of type Integer
   
   * - lodi
     - Integer
     - private field of type Integer
   
   * - nextDayLodi
     - Integer
     - private field of type Integer
   
   * - app
     - Integer
     - private field of type Integer
   
   * - nextDayApp
     - Integer
     - private field of type Integer
   
   * - maternityLeave
     - Integer
     - private field of type Integer
   
   * - suspended
     - Integer
     - private field of type Integer
   
   * - nextDaySuspended
     - Integer
     - private field of type Integer
   
   * - militaryDutyWithPay
     - Integer
     - private field of type Integer
   
   * - militaryDutyWithoutPay
     - Integer
     - private field of type Integer
   
   * - nextDayMilitaryDutyWithoutPay
     - Integer
     - private field of type Integer
   
   * - terminalLeave
     - Integer
     - private field of type Integer
   
   * - nextDayTerminalLeave
     - Integer
     - private field of type Integer
   
   * - civilServiceExam
     - Integer
     - private field of type Integer
   
   * - deathInFamily
     - Integer
     - private field of type Integer
   
   * - honorGuard
     - Integer
     - private field of type Integer
   
   * - juryDuty
     - Integer
     - private field of type Integer
   
   * - familyMedicalLeaveAct
     - Integer
     - private field of type Integer
   
   * - absentWithoutLeave
     - Integer
     - private field of type Integer
   
   * - nextDayAbsentWithoutLeave
     - Integer
     - private field of type Integer
   
   * - compensation
     - Integer
     - private field of type Integer
   
   * - compensationChargedSick
     - Integer
     - private field of type Integer
   
   * - emergencyVacation
     - Integer
     - private field of type Integer
   
   * - vacationForSick
     - Integer
     - private field of type Integer
   
   * - vacationForCompensation
     - Integer
     - private field of type Integer
   
   * - fourDayTempChart
     - Integer
     - private field of type Integer
   
   * - regularDayOff
     - Integer
     - private field of type Integer
   
   * - disability
     - Integer
     - private field of type Integer
   
   * - personal
     - Integer
     - private field of type Integer
   
   * - religious
     - Integer
     - private field of type Integer
   
   * - unionActivity
     - Integer
     - private field of type Integer
   
   * - conferenceAttendance
     - Integer
     - private field of type Integer
   
   * - disciplinary
     - Integer
     - private field of type Integer
   
   * - other
     - Integer
     - private field of type Integer
   
   * - multiple
     - Integer
     - private field of type Integer
   
   * - medicalExcusedLeave
     - Integer
     - private field of type Integer
   
   * - subcategoryShift1Tasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift2Tasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift3Tasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledChartTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledVacationTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledChartAndVacationTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledChartTasksNextDay
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledVacationTasksNextDay
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCancelledChartAndVacationTasksNextDay
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryOvertimeHours
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryOvertimeMinutes
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryCoveredByOverTimeStatuses
     - Map<String, CoveredByOvertimeStatus>
     - private field of type Map<String, CoveredByOvertimeStatus>
   
   * - subcategoryTotalAssignedTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryOvertimeAssignmentTypeTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift1NextDayTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift2NextDayTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift3NextDayTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryTotalAssignedNextDayTasks
     - Map<String, Integer>
     - private field of type Map<String, Integer>
   
   * - subcategoryShift1TasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryShift2TasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryShift3TasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledChartTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledVacationTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledChartAndVacationTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledChartTasksForServiceLocationsNextDay
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledVacationTasksForServiceLocationsNextDay
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCancelledChartAndVacationTasksForServiceLocationsNextDay
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryOvertimeHoursForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryOvertimeMinutesForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryCoveredByOverTimeStatusesForServiceLocations
     - Map<SubcategoryLocationKey, CoveredByOvertimeStatus>
     - private field of type Map<SubcategoryLocationKey, CoveredByOvertimeStatus>
   
   * - subcategoryTotalAssignedTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryShift1NextDayTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryShift2NextDayTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryShift3NextDayTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   
   * - subcategoryTotalAssignedNextDayTasksForServiceLocations
     - Map<SubcategoryLocationKey, Integer>
     - private field of type Map<SubcategoryLocationKey, Integer>
   


**SubcategoryModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for SubcategoryModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - subcategoryCode
     - String
     - private field of type String
   
   * - subcategoryDescription
     - String
     - private field of type String
   
   * - subcategorySortSequence
     - Integer
     - private field of type Integer
   
   * - categoryCorrelationId
     - String
     - private field of type String
   


**CategoryLocationKey**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for CategoryLocationKey

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - category
     - String
     - private field of type String
   
   * - location
     - String
     - private field of type String
   


**PersonnelDateKey**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for PersonnelDateKey

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - personnelId
     - Long
     - private field of type Long
   
   * - date
     - LocalDate
     - private field of type LocalDate
   


**Constants**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for Constants

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**ChildLocation**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for ChildLocation

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - relatedDistricts
     - Set<String>
     - private field of type Set<String>
   


**DetailsDrillThruModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for DetailsDrillThruModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - type
     - String
     - private field of type String
   
   * - col1
     - String
     - private field of type String
   
   * - col2
     - String
     - private field of type String
   
   * - col3
     - String
     - private field of type String
   
   * - col4
     - String
     - private field of type String
   
   * - col5
     - String
     - private field of type String
   
   * - col6
     - String
     - private field of type String
   
   * - col7
     - String
     - private field of type String
   
   * - col8
     - String
     - private field of type String
   
   * - col9
     - String
     - private field of type String
   
   * - col10
     - String
     - private field of type String
   
   * - col11
     - String
     - private field of type String
   
   * - col12
     - String
     - private field of type String
   
   * - col13
     - String
     - private field of type String
   


**CategoryModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for CategoryModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - categoryCode
     - String
     - private field of type String
   
   * - categoryDescription
     - String
     - private field of type String
   
   * - categorySortSequence
     - Integer
     - private field of type Integer
   


**LocationRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for LocationRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - childLocation
     - ChildLocation
     - private field of type ChildLocation
   
   * - payrollAssigned
     - Integer
     - private field of type Integer
   
   * - totalAttached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalDetached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalUnavailable
     - BigDecimal
     - private field of type BigDecimal
   
   * - netPresent
     - BigDecimal
     - private field of type BigDecimal
   
   * - overtimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - startedPreviousDay
     - Integer
     - private field of type Integer
   
   * - workingNextDay
     - Integer
     - private field of type Integer
   
   * - workingNextDayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - overtimeHours
     - Integer
     - private field of type Integer
   
   * - overtimeMinutes
     - Integer
     - private field of type Integer
   
   * - netPresentPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - assignedPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - permanentAttachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentDetachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - workedNightShifts
     - BigDecimal
     - private field of type BigDecimal
   
   * - mechanicsAssigned
     - Integer
     - private field of type Integer
   
   * - mechanicsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - internsAssigned
     - Integer
     - private field of type Integer
   
   * - internsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - jtpAssigned
     - Integer
     - private field of type Integer
   
   * - jtpAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - scheduledCharts
     - Integer
     - private field of type Integer
   
   * - scheduledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - scheduledVacations
     - Integer
     - private field of type Integer
   
   * - scheduledSundays
     - Integer
     - private field of type Integer
   
   * - scheduledHolidays
     - Integer
     - private field of type Integer
   
   * - cancelledSundays
     - Integer
     - private field of type Integer
   
   * - cancelledHolidays
     - Integer
     - private field of type Integer
   
   * - xwpFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - xwopFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwpFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwopFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - lwopXFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - paternityLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - ds95Fraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - latenessFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherExcusedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - sickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - lodiFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - appFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - maternityLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - suspendedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithPayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithoutPayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - terminalLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - civilServiceExamFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - deathInFamilyFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - honorGuardFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - juryDutyFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - familyMedicalLeaveActFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - absentWithoutLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - sundayAndVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationAndChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationChargedSickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - emergencyVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForSickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForCompensationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - fourDayTempChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - regularDayOffFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - disabilityFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - personalFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - religiousFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - unionActivityFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - conferenceAttendanceFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - disciplinaryFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - multipleFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - medicalExcusedLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   


**QuotaKey**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for QuotaKey

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - location
     - String
     - private field of type String
   
   * - subcategory
     - String
     - private field of type String
   


**SubcategoryLocationKey**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for SubcategoryLocationKey

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - subcategory
     - String
     - private field of type String
   
   * - location
     - String
     - private field of type String
   
   * - serviceLocation
     - String
     - private field of type String
   


**LocationModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for LocationModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - locationCode
     - String
     - private field of type String
   
   * - locationDescription
     - String
     - private field of type String
   
   * - locationSortSequence
     - Integer
     - private field of type Integer
   
   * - isDistrictLevel
     - boolean
     - private field of type boolean
   


**SupportedTitleModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model``

*Purpose:* Data model for SupportedTitleModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - code
     - String
     - private field of type String
   
   * - description
     - String
     - private field of type String
   


**PersonnelModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for PersonnelModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - tasks
     - List<PersonnelTaskModel>
     - private field of type List<PersonnelTaskModel>
   
   * - cancelledChartModel
     - UnavailabilityModel
     - private field of type UnavailabilityModel
   
   * - cancelledVacationModel
     - UnavailabilityModel
     - private field of type UnavailabilityModel
   
   * - cancelledSundayModel
     - UnavailabilityModel
     - private field of type UnavailabilityModel
   
   * - cancelledHolidayModel
     - UnavailabilityModel
     - private field of type UnavailabilityModel
   
   * - nextDayTasks
     - List<PersonnelTaskModel>
     - private field of type List<PersonnelTaskModel>
   
   * - nextDayUnavailabilities
     - List<UnavailabilityModel>
     - private field of type List<UnavailabilityModel>
   
   * - permanentDetachmentLocation
     - String
     - private field of type String
   
   * - locationUtilizations
     - Map<String, LocationUtilization>
     - private field of type Map<String, LocationUtilization>
   
   * - cancelledAndRemovedUnavailabilities
     - List<UnavailabilityModel>
     - private field of type List<UnavailabilityModel>
   


**PersonnelDrillTruModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for PersonnelDrillTruModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - id
     - Long
     - private field of type Long
   
   * - name
     - String
     - private field of type String
   
   * - number
     - BigDecimal
     - private field of type BigDecimal
   
   * - homeLocation
     - String
     - private field of type String
   
   * - title
     - String
     - private field of type String
   
   * - comments
     - StringBuilder
     - private field of type StringBuilder
   
   * - details
     - PersonnelDrillTruDetailModel
     - private field of type PersonnelDrillTruDetailModel
   
   * - isOvertime
     - boolean
     - private field of type boolean
   


**UnavailabilityDrillThruModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for UnavailabilityDrillThruModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**UnavailabilityModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for UnavailabilityModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**PersonnelDrillTruDetailModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for PersonnelDrillTruDetailModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**DetachmentModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for DetachmentModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**DetachmentDrillThruModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.personnel``

*Purpose:* Data model for DetachmentDrillThruModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**AbstractPage**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages``

*Purpose:* Data model for AbstractPage

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - errorMessage
     - String
     - private field of type String
   
   * - personnel
     - List<PersonnelDrillTruModel>
     - private field of type List<PersonnelDrillTruModel>
   


**NonSmartPersonnelCount**

*Package:* ``gov.nyc.dsny.reports.utilization.model.opsboard``

*Purpose:* Data model for NonSmartPersonnelCount

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - id
     - BoardId
     - private field of type BoardId
   
   * - anticipatedPresent
     - AnticipatedPresent
     - private field of type AnticipatedPresent
   
   * - assigned
     - Assigned
     - private field of type Assigned
   


**AnticipatedPresent**

*Package:* ``gov.nyc.dsny.reports.utilization.model.opsboard``

*Purpose:* Data model for AnticipatedPresent

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**Assigned**

*Package:* ``gov.nyc.dsny.reports.utilization.model.opsboard``

*Purpose:* Data model for Assigned

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**OpsBoardLock**

*Package:* ``gov.nyc.dsny.reports.utilization.model.opsboard``

*Purpose:* Data model for OpsBoardLock

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - id
     - BoardId
     - private field of type BoardId
   
   * - locked
     - boolean
     - private field of type boolean
   


**TaskDrillThruModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.task``

*Purpose:* Data model for TaskDrillThruModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - identifier
     - String
     - private field of type String
   
   * - boardLocation
     - String
     - private field of type String
   
   * - boardDate
     - LocalDate
     - private field of type LocalDate
   
   * - boardDateString
     - String
     - private field of type String
   
   * - category
     - String
     - private field of type String
   
   * - subcategory
     - String
     - private field of type String
   
   * - serviceLocation
     - String
     - private field of type String
   
   * - assignmentType
     - String
     - private field of type String
   
   * - shiftStart
     - LocalDateTime
     - private field of type LocalDateTime
   
   * - shiftEnd
     - LocalDateTime
     - private field of type LocalDateTime
   
   * - shiftStartString
     - String
     - private field of type String
   
   * - shiftEndString
     - String
     - private field of type String
   
   * - personnelReplacementType
     - String
     - private field of type String
   
   * - overTimeHours
     - Integer
     - private field of type Integer
   
   * - overTimeMinutes
     - Integer
     - private field of type Integer
   
   * - taskTitle
     - String
     - private field of type String
   
   * - taskComments
     - String
     - private field of type String
   
   * - linkParentIdentifier
     - String
     - private field of type String
   


**PersonnelTaskModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.task``

*Purpose:* Data model for PersonnelTaskModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - personnelId
     - Long
     - private field of type Long
   
   * - identifier
     - String
     - private field of type String
   
   * - boardLocation
     - String
     - private field of type String
   
   * - boardDate
     - LocalDate
     - private field of type LocalDate
   
   * - category
     - String
     - private field of type String
   
   * - sequence
     - Long
     - private field of type Long
   
   * - subcategory
     - String
     - private field of type String
   
   * - serviceLocation
     - String
     - private field of type String
   
   * - assignmentType
     - String
     - private field of type String
   
   * - shiftStart
     - LocalDateTime
     - private field of type LocalDateTime
   
   * - shiftEnd
     - LocalDateTime
     - private field of type LocalDateTime
   
   * - personnelReplacementType
     - String
     - private field of type String
   
   * - overTimeHours
     - Integer
     - private field of type Integer
   
   * - overTimeMinutes
     - Integer
     - private field of type Integer
   
   * - title
     - String
     - private field of type String
   
   * - comments
     - String
     - private field of type String
   
   * - linkParentIdentifier
     - String
     - private field of type String
   
   * - nextDay
     - boolean
     - private field of type boolean
   


**WorkUnitModel**

*Package:* ``gov.nyc.dsny.reports.utilization.model.task``

*Purpose:* Data model for WorkUnitModel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - code
     - String
     - private field of type String
   
   * - description
     - String
     - private field of type String
   


**SummaryWidgetRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.summary``

*Purpose:* Data model for SummaryWidgetRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - location
     - ChildLocation
     - private field of type ChildLocation
   
   * - payrollAssigned
     - Integer
     - private field of type Integer
   
   * - totalAttached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalDetached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalUnavailable
     - BigDecimal
     - private field of type BigDecimal
   
   * - netPresent
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalOvertimeHours
     - Integer
     - private field of type Integer
   
   * - totalOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - netPresentPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - assignedPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - startedPreviousDay
     - Integer
     - private field of type Integer
   
   * - workingNextDay
     - Integer
     - private field of type Integer
   
   * - permanentAttachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentDetachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - workedNightShifts
     - BigDecimal
     - private field of type BigDecimal
   
   * - mechanicsAssigned
     - Integer
     - private field of type Integer
   
   * - mechanicsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - internsAssigned
     - Integer
     - private field of type Integer
   
   * - internsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - jtpAssigned
     - Integer
     - private field of type Integer
   
   * - jtpAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - isDrillThruAllowed
     - boolean
     - private field of type boolean
   


**OtherWidgetTotals**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.summary``

*Purpose:* Data model for OtherWidgetTotals

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - workedNightShifts
     - BigDecimal
     - private field of type BigDecimal
   
   * - mechanicsAssigned
     - Integer
     - private field of type Integer
   
   * - mechanicsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - internsAssigned
     - Integer
     - private field of type Integer
   
   * - internsAnticipatedPresent
     - Integer
     - private field of type Integer
   
   * - jtpAssigned
     - Integer
     - private field of type Integer
   
   * - jtpAnticipatedPresent
     - Integer
     - private field of type Integer
   


**SummaryPage**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.summary``

*Purpose:* Data model for SummaryPage

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - locationRows
     - Map<String, LocationRow>
     - private field of type Map<String, LocationRow>
   
   * - summaryWidgetRows
     - List<SummaryWidgetRow>
     - private field of type List<SummaryWidgetRow>
   
   * - summaryWidgetTotals
     - SummaryWidgetTotals
     - private field of type SummaryWidgetTotals
   
   * - availabilityWidgetTotals
     - AvailabilityWidgetTotals
     - private field of type AvailabilityWidgetTotals
   
   * - otherWidgetTotals
     - OtherWidgetTotals
     - private field of type OtherWidgetTotals
   


**AvailabilityWidgetTotals**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.summary``

*Purpose:* Data model for AvailabilityWidgetTotals

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - permanentAttachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryAttachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - permanentDetachments
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsWithinZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - temporaryDetachmentsOutOfZone
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   


**SummaryWidgetTotals**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.summary``

*Purpose:* Data model for SummaryWidgetTotals

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - payrollAssigned
     - Integer
     - private field of type Integer
   
   * - totalAttached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalDetached
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - totalUnavailable
     - BigDecimal
     - private field of type BigDecimal
   
   * - netPresent
     - BigDecimal
     - private field of type BigDecimal
   
   * - overtimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - overtimeHours
     - Integer
     - private field of type Integer
   
   * - overtimeMinutes
     - Integer
     - private field of type Integer
   
   * - netPresentPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - assignedPlusOvertime
     - BigDecimal
     - private field of type BigDecimal
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - startedPreviousDay
     - Integer
     - private field of type Integer
   
   * - workingNextDay
     - Integer
     - private field of type Integer
   


**LocationUtilizationWidgetRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for LocationUtilizationWidgetRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - location
     - Location
     - private field of type Location
   
   * - locationId
     - String
     - private field of type String
   
   * - locationSequence
     - Integer
     - private field of type Integer
   
   * - categoryLocationUtilizationRows
     - List<CategoryLocationUtilizationRow>
     - private field of type List<CategoryLocationUtilizationRow>
   
   * - quota
     - Integer
     - private field of type Integer
   
   * - subcategoryAssignedVsQuota
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryTotalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift1Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift2Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift3Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeHours
     - Integer
     - private field of type Integer
   
   * - subcategoryOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - subcategoryCancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - coveredByOvertimeStatus
     - CoveredByOvertimeStatus
     - private field of type CoveredByOvertimeStatus
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   


**CategoryLocationUtilizationRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for CategoryLocationUtilizationRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - categoryLocationKey
     - CategoryLocationKey
     - private field of type CategoryLocationKey
   
   * - categoryModel
     - CategoryModel
     - private field of type CategoryModel
   
   * - location
     - Location
     - private field of type Location
   
   * - locationId
     - String
     - private field of type String
   
   * - locationSequence
     - Integer
     - private field of type Integer
   
   * - subcategotyChildUtilizationRows
     - List<SubcategoryChildLocationUtilizationRow>
     - private field of type List<SubcategoryChildLocationUtilizationRow>
   
   * - quota
     - Integer
     - private field of type Integer
   
   * - subcategoryAssignedVsQuota
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryTotalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift1Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift2Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift3Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeHours
     - Integer
     - private field of type Integer
   
   * - subcategoryOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - subcategoryCancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - coveredByOvertimeStatus
     - CoveredByOvertimeStatus
     - private field of type CoveredByOvertimeStatus
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   


**SubcategoryChildLocationUtilizationRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for SubcategoryChildLocationUtilizationRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - subcategoryLocationKey
     - SubcategoryLocationKey
     - private field of type SubcategoryLocationKey
   
   * - subcategoryModel
     - SubcategoryModel
     - private field of type SubcategoryModel
   
   * - childLocation
     - ChildLocation
     - private field of type ChildLocation
   
   * - subcategotyUtilizationRows
     - List<SubcategoryLocationUtilizationRow>
     - private field of type List<SubcategoryLocationUtilizationRow>
   
   * - quota
     - Integer
     - private field of type Integer
   
   * - subcategoryAssignedVsQuota
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryTotalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift1Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift2Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift3Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeHours
     - Integer
     - private field of type Integer
   
   * - subcategoryOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - subcategoryCancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - coveredByOvertimeStatus
     - CoveredByOvertimeStatus
     - private field of type CoveredByOvertimeStatus
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   


**UtilizationPage**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for UtilizationPage

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - subcategoryUtilizationRows
     - List<SubcategoryLocationUtilizationRow>
     - private field of type List<SubcategoryLocationUtilizationRow>
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - locationUtilizationTotalWidgetRow
     - LocationUtilizationTotalWidgetRow
     - private field of type LocationUtilizationTotalWidgetRow
   
   * - locationUtilizationWidgetRows
     - List<LocationUtilizationWidgetRow>
     - private field of type List<LocationUtilizationWidgetRow>
   
   * - location
     - String
     - private field of type String
   
   * - subcategory
     - String
     - private field of type String
   


**SubcategoryLocationUtilizationRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for SubcategoryLocationUtilizationRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - subcategoryLocationKey
     - SubcategoryLocationKey
     - private field of type SubcategoryLocationKey
   
   * - subcategoryModel
     - SubcategoryModel
     - private field of type SubcategoryModel
   
   * - categoryModel
     - CategoryModel
     - private field of type CategoryModel
   
   * - locationModel
     - LocationModel
     - private field of type LocationModel
   
   * - mainLocationCode
     - String
     - private field of type String
   
   * - mainLocationDescription
     - String
     - private field of type String
   
   * - mainlocationSortSequence
     - Integer
     - private field of type Integer
   
   * - locationCode
     - String
     - private field of type String
   
   * - locationDescription
     - String
     - private field of type String
   
   * - locationSortSequence
     - Integer
     - private field of type Integer
   
   * - categoryCode
     - String
     - private field of type String
   
   * - categoryDescription
     - String
     - private field of type String
   
   * - categorySortSequence
     - Integer
     - private field of type Integer
   
   * - subcategoryCode
     - String
     - private field of type String
   
   * - subcategoryDescription
     - String
     - private field of type String
   
   * - subcategorySortSequence
     - Integer
     - private field of type Integer
   
   * - serviceLocationCode
     - String
     - private field of type String
   
   * - serviceLocationDescription
     - String
     - private field of type String
   
   * - serviceLocationSortSequence
     - Integer
     - private field of type Integer
   
   * - quota
     - Integer
     - private field of type Integer
   
   * - subcategoryAssignedVsQuota
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryTotalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift1Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift2Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift3Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeHours
     - Integer
     - private field of type Integer
   
   * - subcategoryOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - subcategoryCancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCoveredByOverTimeStatus
     - CoveredByOvertimeStatus
     - private field of type CoveredByOvertimeStatus
   
   * - isDrillThruAllowed
     - boolean
     - private field of type boolean
   


**LocationUtilizationTotalWidgetRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.utilization``

*Purpose:* Data model for LocationUtilizationTotalWidgetRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - location
     - Location
     - private field of type Location
   
   * - locationId
     - String
     - private field of type String
   
   * - locationSequence
     - Integer
     - private field of type Integer
   
   * - rootLocationCategoryRows
     - List<CategoryLocationUtilizationRow>
     - private field of type List<CategoryLocationUtilizationRow>
   
   * - quota
     - Integer
     - private field of type Integer
   
   * - subcategoryAssignedVsQuota
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryTotalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift1Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift2Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryShift3Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeHours
     - Integer
     - private field of type Integer
   
   * - subcategoryOvertimeMinutes
     - Integer
     - private field of type Integer
   
   * - subcategoryCancelledChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAndChartsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryCancelledVacationsAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - subcategoryOvertimeTasks
     - BigDecimal
     - private field of type BigDecimal
   
   * - coveredByOvertimeStatus
     - CoveredByOvertimeStatus
     - private field of type CoveredByOvertimeStatus
   


**UnavailabilityLocationRow**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.unavailability``

*Purpose:* Data model for UnavailabilityLocationRow

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - location
     - ChildLocation
     - private field of type ChildLocation
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - charts
     - Integer
     - private field of type Integer
   
   * - scheduledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - vacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - scheduledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - vacations
     - Integer
     - private field of type Integer
   
   * - scheduledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - sundays
     - Integer
     - private field of type Integer
   
   * - scheduledSundays
     - Integer
     - private field of type Integer
   
   * - cancelledSundays
     - Integer
     - private field of type Integer
   
   * - holidays
     - Integer
     - private field of type Integer
   
   * - scheduledHolidays
     - Integer
     - private field of type Integer
   
   * - cancelledHolidays
     - Integer
     - private field of type Integer
   
   * - xwpFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - xwopFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - sickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - lodiFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - appFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - maternityLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - suspendedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithPayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithoutPayFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - terminalLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - civilServiceExamFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - deathInFamilyFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - honorGuardFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - juryDutyFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - familyMedicalLeaveActFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - absentWithoutLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - sundayAndVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationAndChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationChargedSickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - emergencyVacationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForSickFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForCompensationFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - fourDayTempChartFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - regularDayOffFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - disabilityFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - personalFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - religiousFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - unionActivityFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - conferenceAttendanceFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwpFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwopFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - lwopXFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - paternityLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - ds95Fraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - latenessFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherExcusedFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - disciplinaryFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - multipleFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - medicalExcusedLeaveFraction
     - BigDecimal
     - private field of type BigDecimal
   
   * - total
     - BigDecimal
     - private field of type BigDecimal
   
   * - isDrillThruAllowed
     - boolean
     - private field of type boolean
   


**UnavailabilityPage**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.unavailability``

*Purpose:* Data model for UnavailabilityPage

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - unavailabilityLocationRows
     - List<UnavailabilityLocationRow>
     - private field of type List<UnavailabilityLocationRow>
   
   * - unavailabilityWidgetTotals
     - UnavailabilityWidgetTotals
     - private field of type UnavailabilityWidgetTotals
   


**UnavailabilityWidgetTotals**

*Package:* ``gov.nyc.dsny.reports.utilization.model.pages.unavailability``

*Purpose:* Data model for UnavailabilityWidgetTotals

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   
   * - boardLockStatus
     - BoardLockStatus
     - private field of type BoardLockStatus
   
   * - charts
     - Integer
     - private field of type Integer
   
   * - scheduledCharts
     - Integer
     - private field of type Integer
   
   * - cancelledCharts
     - Integer
     - private field of type Integer
   
   * - vacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - scheduledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - cancelledVacationsAndCharts
     - Integer
     - private field of type Integer
   
   * - vacations
     - Integer
     - private field of type Integer
   
   * - scheduledVacations
     - Integer
     - private field of type Integer
   
   * - cancelledVacations
     - Integer
     - private field of type Integer
   
   * - sundays
     - Integer
     - private field of type Integer
   
   * - scheduledSundays
     - Integer
     - private field of type Integer
   
   * - cancelledSundays
     - Integer
     - private field of type Integer
   
   * - holidays
     - Integer
     - private field of type Integer
   
   * - scheduledHolidays
     - Integer
     - private field of type Integer
   
   * - cancelledHolidays
     - Integer
     - private field of type Integer
   
   * - xwpAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - xwopAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwpAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - cvXwopAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - paternityLeaveAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - lwopXAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - ds95Assigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - latenessAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherExcusedAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - sickAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - lodiAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - appAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - maternityLeaveAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - suspendedAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithPayAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - militaryDutyWithoutPayAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - terminalLeaveAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - civilServiceExamAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - deathInFamilyAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - honorGuardAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - juryDutyAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - familyMedicalLeaveActAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - absentWithoutLeaveAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - sundayAndVacationAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndChartAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - holidayAndVacationAndChartAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - compensationChargedSickAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - emergencyVacationAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForSickAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - vacationForCompensationAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - fourDayTempChartAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - regularDayOffAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - disabilityAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - personalAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - religiousAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - unionActivityAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - conferenceAttendanceAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - disciplinaryAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - otherAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - multipleAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - medicalExcusedLeaveAssigned
     - BigDecimal
     - private field of type BigDecimal
   
   * - total
     - BigDecimal
     - private field of type BigDecimal
   


**Personnel**

*Package:* ``gov.nyc.dsny.reports.utilization.domain``

*Purpose:* Data model for Personnel

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   


**Task**

*Package:* ``gov.nyc.dsny.reports.utilization.domain``

*Purpose:* Data model for Task

.. list-table:: Fields
   :header-rows: 1
   :widths: 30 20 50

   * - Field Name
     - Type
     - Description
   



Service Architecture
-------------------

Application Structure
~~~~~~~~~~~~~~~~~~~~

.. graphviz::

   digraph service_architecture {
       rankdir=TB;
       node [shape=rectangle, style=filled];
       
       // Presentation Layer
       endpoint [label="SOAP Endpoints\\nhttp://utilization.reports.dsny.nyc.gov/", fillcolor=lightblue];
       
       // Service Layer  
       
       webserviceconfiguration [label="WebServiceConfiguration\\nWebServiceConfiguration", fillcolor=lightgreen];
       
       opsboardserviceimpl [label="OpsBoardServiceImpl\\nOpsBoardServiceImpl", fillcolor=lightgreen];
       
       personnelserviceimpl [label="PersonnelServiceImpl\\nPersonnelServiceImpl", fillcolor=lightgreen];
       
       reportsummaryserviceimpl [label="ReportSummaryServiceImpl\\nReportSummaryServiceImpl", fillcolor=lightgreen];
       
       taskserviceimpl [label="TaskServiceImpl\\nTaskServiceImpl", fillcolor=lightgreen];
       
       reportutilizationserviceimpl [label="ReportUtilizationServiceImpl\\nReportUtilizationServiceImpl", fillcolor=lightgreen];
       
       personneldrillthruserviceimpl [label="PersonnelDrillThruServiceImpl\\nPersonnelDrillThruServiceImpl", fillcolor=lightgreen];
       
       reportunavailabilityserviceimpl [label="ReportUnavailabilityServiceImpl\\nReportUnavailabilityServiceImpl", fillcolor=lightgreen];
       
       quotaserviceimpl [label="QuotaServiceImpl\\nQuotaServiceImpl", fillcolor=lightgreen];
       
       subcategoryserviceimpl [label="SubcategoryServiceImpl\\nSubcategoryServiceImpl", fillcolor=lightgreen];
       
       categoryserviceimpl [label="CategoryServiceImpl\\nCategoryServiceImpl", fillcolor=lightgreen];
       
       unavailabilitytypeserviceimpl [label="UnavailabilityTypeServiceImpl\\nUnavailabilityTypeServiceImpl", fillcolor=lightgreen];
       
       locationserviceimpl [label="LocationServiceImpl\\nLocationServiceImpl", fillcolor=lightgreen];
       
       utilizationpage [label="UtilizationPage\\nUtilizationPage", fillcolor=lightgreen];
       
       
       // Repository Layer
         
       utilizationquotarepository [label="UtilizationQuotaRepository", fillcolor=yellow];
         
       opsboardrepository [label="OpsBoardRepository", fillcolor=yellow];
         
       taskrepository [label="TaskRepository", fillcolor=yellow];
         
       personnelrepository [label="PersonnelRepository", fillcolor=yellow];
       
       
       // External Systems
       database [label="Database\\nUnknown", fillcolor=pink];
       
       // Connections
       endpoint -> webserviceconfiguration;
       endpoint -> opsboardserviceimpl;
       endpoint -> personnelserviceimpl;
       endpoint -> reportsummaryserviceimpl;
       endpoint -> taskserviceimpl;
       endpoint -> reportutilizationserviceimpl;
       endpoint -> personneldrillthruserviceimpl;
       endpoint -> reportunavailabilityserviceimpl;
       endpoint -> quotaserviceimpl;
       endpoint -> subcategoryserviceimpl;
       endpoint -> categoryserviceimpl;
       endpoint -> unavailabilitytypeserviceimpl;
       endpoint -> locationserviceimpl;
       endpoint -> utilizationpage;
       
       
       
       
       opsboardserviceimpl -> opsboardrepository;
       
       
       
       personnelserviceimpl -> personnelrepository;
       
       
       
       
       
       taskserviceimpl -> taskrepository;
       
       
       
       
       
       
       
       
       
       quotaserviceimpl -> utilizationquotarepository;
       
       
       
       subcategoryserviceimpl -> subcategoryrepository;
       
       
       
       categoryserviceimpl -> categoryrepository;
       
       
       
       unavailabilitytypeserviceimpl -> unavailabilitytyperepository;
       
       
       
       locationserviceimpl -> locationrepository;
       
       
       
       
       
       utilizationquotarepository -> database;
       
       opsboardrepository -> database;
       
       taskrepository -> database;
       
       personnelrepository -> database;
       
   }

Configuration Files
~~~~~~~~~~~~~~~~~~

.. list-table:: Key Configuration Locations
   :header-rows: 1
   :widths: 40 60

   * - File
     - Purpose
   * - ``application.properties``
     - Server port, context path, JMX settings
   * - ``logback.xml``
     - Logging configuration
   * - ``web.xml`` (if present)
     - Web application deployment descriptor

Environment Variables
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Server Configuration
   SERVER_PORT=8080
   SERVER_CONTEXT_PATH=/
   
   # Database Configuration (if applicable)
   DB_URL=TODO: Add database URL
   DB_USERNAME=TODO: Add database username
   DB_PASSWORD=TODO: Add database password
   
   # Logging Configuration
   LOG_LEVEL=INFO

.. important::
   **Configuration Management**: All sensitive configuration should be externalized.
   Never hardcode credentials or environment-specific values.

Testing & Usage Examples
-----------------------

Testing Strategy
~~~~~~~~~~~~~~~

.. list-table:: Testing Approaches
   :header-rows: 1
   :widths: 30 70

   * - Test Type
     - Approach
   * - Unit Testing
     - Test service layer methods with mocked dependencies
   * - Integration Testing
     - Test complete endpoint-to-database flow
   * - SOAP Testing
     - Use SoapUI or Postman with WSDL import
   * - Load Testing
     - Test endpoint performance under expected load

SOAP Client Examples
~~~~~~~~~~~~~~~~~~~

**Java Client Example:**

.. code-block:: java

   // Using JAX-WS
   UtilizationService service = new UtilizationService();
   UtilizationServicePortType port = service.getUtilizationServiceHttpPort();
   
   // Example call
   
   SupportedTitleModel result = port.getSupportedTitles();
   

**Python Client Example:**

.. code-block:: python

   from zeep import Client
   
   client = Client('http://localhost:8080/UtilizationService?wsdl')
   
   # Example call
   
   result = client.service.getSupportedTitles()
   

**cURL Example:**

.. code-block:: bash

   curl -X POST "http://localhost:8080/UtilizationService" \
        -H "Content-Type: text/xml; charset=utf-8" \
        -H "SOAPAction: \"http://utilization.reports.dsny.nyc.gov//getSupportedTitles\"" \
        -d @request.xml

Common Issues & Troubleshooting
------------------------------

Endpoint Issues
~~~~~~~~~~~~~~

**Service Unavailable (503)**

*Symptoms:* Endpoint returns 503 or connection refused

*Investigation Steps:*

1. Check if service is running: ``ps aux | grep java``
2. Verify port is listening: ``netstat -tlnp | grep 8080``
3. Check application logs for startup errors
4. Verify database connectivity (if applicable)

.. code-block:: bash

   # Check service status
   curl -I http://localhost:8080/actuator/health  # If Spring Boot Actuator enabled
   
   # Check WSDL availability
   curl http://localhost:8080/UtilizationService?wsdl

**SOAP Fault Responses**

*Symptoms:* Receiving SOAP fault instead of expected response

*Investigation Steps:*

1. Validate request XML against WSDL schema
2. Check parameter data types and required fields
3. Verify namespace declarations in request
4. Review application logs for detailed error messages

.. warning::
   **SOAP Debugging**: Always validate your SOAP requests against the WSDL schema.
   Use tools like SoapUI for request validation and testing.

Performance Issues
~~~~~~~~~~~~~~~~~

**Slow Response Times**

*Symptoms:* Endpoints taking >5 seconds to respond

*Investigation Steps:*

1. Check database query performance (if applicable)
2. Monitor JVM garbage collection
3. Review connection pool configuration
4. Check for deadlocks in application logs

.. code-block:: bash

   # Monitor JVM performance
   jstat -gc [pid] 5s
   
   # Check database connections (if applicable)
   # Application-specific monitoring commands

Data Issues
~~~~~~~~~~

**Invalid Response Format**

*Symptoms:* Unexpected response structure or missing fields

*Investigation Steps:*

1. Verify data model mappings in service layer
2. Check for null handling in response objects
3. Validate database schema matches model expectations
4. Review serialization configuration

Deployment & Maintenance
-----------------------

.. warning::
   **All production changes must follow established change management process.**

**Deployment Checklist:**

* ✅ Service builds successfully with ``./gradlew build``
* ✅ Unit tests pass with ``./gradlew test``
* ✅ Integration tests pass in staging environment
* ✅ WSDL is accessible after deployment
* ✅ Health checks return successful status
* ✅ Database migrations completed (if applicable)
* ✅ Configuration files updated for target environment

**Maintenance Tasks:**

* **Weekly**: Review application logs for errors and warnings
* **Monthly**: Check JVM memory usage and garbage collection performance  
* **Quarterly**: Review endpoint performance metrics and optimize slow queries

Emergency Contacts & Escalation
------------------------------

.. list-table:: Contact Information
   :header-rows: 1
   :widths: 25 35 20 20

   * - Role
     - Name
     - Email
     - Phone
   * - Lead Developer
     - TBD
     - TBD
     - TBD
   * - System Administrator
     - TBD
     - TBD
     - TBD
   * - Client Technical Contact
     - TBD
     - TBD
     - TBD

**Escalation Path:**

1. **Severity 1** (Service Down): Immediate call to Lead Developer + System Administrator
2. **Severity 2** (Performance Issues): Email Lead Developer, escalate after 2 hours  
3. **Severity 3** (Minor Issues): Email Lead Developer during business hours

Links & References
-----------------

* **Service WSDL**: http://localhost:8080/UtilizationService?wsdl
* **Source Code**: TBD
* **Build System**: TBD
* **Monitoring**: TBD
* **Issue Tracking**: TBD

---

.. footer::

   *Document generated using Infrastructure Documentation Standards*
   
   :Template: java-api-service.rst v1.0
   :Generated: 2024-01-01
   :Next Review: 2024-04-01
   :Contact: Infrastructure Documentation Team