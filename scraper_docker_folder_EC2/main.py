from webscraper import BGGScraper
from local_save import LocalSave
import export_to_rds
from export_to_S3 import S3ExporterLocal, S3ExporterDirect



if __name__ == "__main__":
    # 'Block 1' code below to be used if user input desired, otherwise 'Block 2' code runs scraper logic with no user inpur required.
    # when running Block 2, refactor webscraper.py BGGScraper class self.category variable (found within __init__ method) to scrape desired data accordingly. 
    
    # Block 1:
    # bgg_scrape = BGGScraper()
    # bgg_scrape.run('//*[@id="c-p-bn"]')
    # save_option = input("Enter 'L' to store data locally, 'C' to upload data to cloud or 'B' to do both: ").capitalize()
    
    # if save_option == 'L':
    #     data_save = LocalSave(bgg_scrape.game_dict)
    #     data_save.run()
    # elif save_option == 'C':
    #     direct_data_export = S3ExporterDirect('data-collection-project-bucket', bgg_scrape.game_dict)
    #     direct_data_export.export_json()
    #     direct_data_export.export_image()
    # elif save_option == 'B':
    #     data_save = LocalSave(bgg_scrape.game_dict)
    #     data_save.run()
    #     local_data_export = S3ExporterLocal('./raw_data','data-collection-project-bucket')
    #     local_data_export.export_to_bucket()
    # else:
    #     print ('Data not saved')
    #     pass
    #     #TODO: give user option to renter save choice
    
    # if input("Enter 'Y' to upload data to RDS table: ").capitalize() == 'Y':
    #     export_to_rds.run_rds_export(bgg_scrape.game_dict)
    # else:
    #     print('Data not uploaded to RDS')
    #     pass

    # Block 2:
    bgg_scrape = BGGScraper()
    bgg_scrape.run('//*[@id="c-p-bn"]') # run scraper
    data_save = LocalSave(bgg_scrape.game_dict)
    data_save.run() # save scraped data locally
    direct_data_export = S3ExporterDirect('data-collection-project-bucket', bgg_scrape.game_dict)
    direct_data_export.export_json() # export scraped data to S3 bucket
    direct_data_export.export_image() # export scraped image data to S3 bucket
    export_to_rds.run_rds_export(bgg_scrape.game_dict) # export scraped data to RDS
