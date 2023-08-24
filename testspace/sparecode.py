        # print(f"query: {result['result']['query']}")
        # print(f"project kind: {result['result']['prediction']['projectKind']}\n")

        # print(f"top intent: {result['result']['prediction']['topIntent']}")
        # print(f"category: {result['result']['prediction']['intents'][0]['category']}")
        # print(f"confidence score: {result['result']['prediction']['intents'][0]['confidenceScore']}\n")

        # print("entities:")
        # for entity in result['result']['prediction']['entities']:
        #     print(f"\ncategory: {entity['category']}")
        #     print(f"text: {entity['text']}")
        #     print(f"confidence score: {entity['confidenceScore']}")
        #     if "resolutions" in entity:
        #         print("resolutions")
        #         for resolution in entity['resolutions']:
        #             print(f"kind: {resolution['resolutionKind']}")
        #             print(f"value: {resolution['value']}")
        #     if "extraInformation" in entity:
        #         print("extra info")
        #         for data in entity['extraInformation']:
        #             print(f"kind: {data['extraInformationKind']}")
        #             if data['extraInformationKind'] == "ListKey":
        #                 print(f"key: {data['key']}")
        #             if data['extraInformationKind'] == "EntitySubtype":
        #                 print(f"value: {data['value']}")