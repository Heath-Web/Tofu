import pandas as pd

company_info = {
  "Company Name": {
    "data": [
      {
        "id": "859cf3c3-8025-4e3c-8a83-892df7bc8136",
        "type": "text",
        "value": "Stampli"
      }
    ]
  },
  "Company Website": {
    "data": [
      {
        "id": "53300d1d-0c22-4b0c-a8e8-ec7658f06fe8",
        "type": "url",
        "value": "https://www.stampli.com/"
      }
    ]
  },
  "Product Overview": {
    "data": [
      {
        "id": "0b6e1d04-67b3-494b-957c-07e0a6b3e941",
        "type": "text",
        "value": "Stampli is the only AP automation solution that’s purpose-built for Accounts Payable. It centers all communication, documentation, and workflows on top of each invoice, eliminating the need for workarounds, external communications channels, 3rd-party solutions, or manual AP work inside the ERP. Every activity is logged and auditable, making month-end close simple and efficient. Stampli also offers AP teams full visibility into the status of every single invoice and payment.\n\nAP teams dramatically reduce tedious manual tasks with the help of Billy the Bot™, Stampli’s AI-powered automation. Billy quickly learns how your business AP processes work to automate your most time-consuming activities, including invoice capture, coding, approvals, fraud detection, and automatic sync of invoice data to your ERP.  \n\nBeyond AP, Stampli offers a suite of integrated products that extend the same levels of efficiency, visibility, and control to direct payments (check, ACH, and credit card), your physical and virtual credit card program, vendor management, and more. \n"
      }
    ]
  },
  "Official Overview ": {
    "data": [
      {
        "id": "19a30063-1e31-407a-8634-7ca8c9f9c221",
        "type": "text",
        "value": "Stampli provides complete visibility and control over your entire AP program. It reduces the risk of errors, fraud, and compliance issues while improving vendor relationships and making your AP processes much more efficient.\n"
      }
    ]
  },
  "Company Description": {
    "data": [
      {
        "id": "04b16677-cb1e-48b3-b0ea-d134def729a4",
        "type": "text",
        "value": "Stampli's AI-powered Accounts Payable automation solution brings all AP-related communication, documentation, and workflows into one place. Automate Accounts Payable without reworking your ERP. Only Stampli supports all native functionality for more than 70 ERPs. You’ll make AP far more efficient without changing your processes."
      }
    ]
  },
  "Stampli differentiators": {
    "data": [
      {
        "id": "9fee94d6-f676-4854-a0d3-9a08cca44c29",
        "type": "text",
        "value": "Least disruption: No need to rework your ERP or change your AP processes.\n\nMost control: One place for all your communication, documentation, and workflows.\n\nSmartest AI: Billy the Bot assists you across the entire invoice process — and he’s always learning.\n\nFastest to value: Stampli deploys in days, not months, with minimal user training.\n\nMore than just AP: Stampli offers integrated payments, credit cards, vendor management, and more."
      }
    ]
  }
}

target_info = {
  "YMCA": {
    "data": [
      {
        "id": "eca59ffa-1c58-45d9-8a9d-e94d4eee28d1",
        "type": "url",
        "value": "https://www.ymca.org/"
      }
    ]
  },
  "Apex Oil": {
    "data": [
      {
        "id": "955ed9e1-b6f8-41ae-af55-8fda5b45dd4f",
        "type": "text",
        "value": "Apex Oil Company, Inc. provides wholesale distribution, storage and transportation of petroleum products"
      },
      {
        "id": "22ee2c6c-ce38-4c04-9e6b-2b719adbb895",
        "type": "url",
        "value": "https://apexoil.com/"
      }
    ]
  },
#   "SmartRoof": {
#     "data": [
#       {
#         "id": "1c086e7d-abe5-43ad-a243-f735ad8b12ca",
#         "type": "text",
#         "value": "SmartRoof believes everyone deserves to reach their potential and live out the AmericanDream."
#       },
#       {
#         "id": "9c8740be-1570-4f99-b2e9-5e6b8a6e54ca",
#         "type": "url",
#         "value": "https://smartroofinc.com/#gref"
#       }
#     ]
#   },
  "Morris Home": {
    "data": [
      {
        "id": "548c3794-3c66-4421-8633-fba71c21d3ca",
        "type": "text",
        "value": "Morris Home makes it easy for you to create the home of your dreams. "
      },
      {
        "id": "f08f88d1-2bfa-4cf2-a603-cc3b69ef5b46",
        "type": "url",
        "value": "https://www.morrisathome.com/about-us"
      }
    ]
  },
  "MegaMex Foods": {
    "data": [
      {
        "id": "eb7b820b-b01c-476f-8e7a-369fffe92951",
        "type": "text",
        "value": ""
      },
      {
        "id": "8ab62cb5-3286-48b7-9f20-502b183a350b",
        "type": "url",
        "value": "https://www.megamexfoods.com/"
      }
    ]
  },
  "Empower Brands": {
    "data": [
      {
        "id": "1e02e8b1-987c-464d-af10-156bda1b6a6c",
        "type": "text",
        "value": ""
      },
      {
        "id": "5bff041f-6d85-4566-929d-c0bed0b7cb5a",
        "type": "url",
        "value": "https://empowerfranchising.com/"
      }
    ]
  },
  "Prysmian Group": {
    "data": [
      {
        "id": "5f533679-574f-4298-bc98-dca184d3fc43",
        "type": "text",
        "value": ""
      },
      {
        "id": "140b9f32-49bd-4f7b-84ce-378531cd144b",
        "type": "url",
        "value": "https://www.prysmiangroup.com/en"
      }
    ]
  },
  "Pappas Restaurants": {
    "data": [
      {
        "id": "73315798-9a08-45c8-9a97-c4dc6d287ea8",
        "type": "text",
        "value": ""
      },
      {
        "id": "e3a47df6-8bb3-43a9-a183-8cf517454f36",
        "type": "url",
        "value": "https://www.pappas.com/"
      }
    ]
  }
}

original_text = ["Preparing for a recession toolkit", 
                 "A recession readiness toolkit to guide CFOs and finance leaders through recessions and periods of economic instability.",
                 "\"2022 CFO Recession Toolkit\"", 
                 "Managers are dealing with a number of economic issues, and some analysts believe that the US is headed toward a recession.<br><br>To respond to the challenge, take action to address a possible recession now, so that you’re ready to minimize the impact and outperform competitors who are not proactive."]
                  
def parse_company_info(company_info):
    company = {}
    for key, value in company_info.items():
        entry = value.get("data", [])
        if entry:
            company[key.strip()] = entry[0]["value"].strip()
    return company

def parse_target_info(target_info:dict):
    target_data = []
    for company_name, fields in target_info.items():
        company_entry = {"name": company_name, "description": "", "url": ""}
        for item in fields["data"]:
            if item["type"] == "text":
                company_entry["description"] = item["value"].strip()
            elif item["type"] == "url":
                company_entry["url"] = item["value"].strip()
        target_data.append(company_entry)
    return target_data

if __name__ == "__main__":
    clean_company_info = parse_company_info(company_info)
    clean_target_info = parse_target_info(target_info)
    print(clean_company_info)
    print(clean_target_info)