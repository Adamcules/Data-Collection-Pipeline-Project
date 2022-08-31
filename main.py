from webscraper import BGGScraper
from local_save import LocalSave
import export_to_rds
from export_to_S3 import S3ExporterLocal, S3ExporterDirect



if __name__ == "__main__":
    bgg_scrape = BGGScraper()
    bgg_scrape.run('//*[@id="c-p-bn"]')
    save_option = input("Enter 'L' to store data locally, 'C' to upload data to cloud or 'B' to do both: ").capitalize()
    
    if save_option == 'L':
        data_save = LocalSave(bgg_scrape.game_dict)
        data_save.run()
    elif save_option == 'C':
        direct_data_export = S3ExporterDirect('data-collection-project-bucket', bgg_scrape.game_dict)
        direct_data_export.export_json()
        direct_data_export.export_image()
    elif save_option == 'B':
        data_save = LocalSave(bgg_scrape.game_dict)
        data_save.run()
        local_data_export = S3ExporterLocal('./raw_data','data-collection-project-bucket')
        local_data_export.export_to_bucket()
    
    export_to_rds.run(bgg_scrape.game_dict)
