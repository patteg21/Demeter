        # try:
        #     entityName = result['result']['prediction']['entities'][1]['text']
        # except IndexError:
        #     entityName = ""

        # if "Dasher" in entityName:
        #     # grabs the number associated with that dasher
        #     _ , dasherNumber = entityName.split(" ")

        #     dasher = Dasher.objects.get(dasherID=dasherNumber)

        #     demeterOutput = f"{dasher} is at {dasher.location}"

        #     return render(request,"inhabitant/home.html",{
        #         "demeterOutput":demeterOutput,