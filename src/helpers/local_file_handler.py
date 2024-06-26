import os
import json
import logging

from ..settings import settings

settings.configure_logging()
logger = logging.getLogger(__name__)

def save_file(json_data, project_id) -> None:
    logger.debug("Saving to disk")
    try:
        directory_path = os.path.join(os.getcwd(), 
                                      settings.FILE_STORAGE_PATH, 
                                      project_id)
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        file_path = os.path.join(directory_path, 'data.json')
        logger.info(f"Saving to {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
    except FileNotFoundError:
        logger.warn(f"File not found {file_path}")
        
def read_file(project_id):
    try:
        directory_path = os.path.join(os.getcwd(), 
                                      settings.FILE_STORAGE_PATH, 
                                      project_id)
        file_path = os.path.join(directory_path, 'data.json')
        f = open(file_path)
        json_data = json.load(f)
        return json_data
    except FileNotFoundError: 
        print("File not found, returning empty")
        return None
    
def save_lock_file(project_id: int, lock):
    logger.debug("Saving lock to disk")
    try:
        directory_path = os.path.join(os.getcwd(), 
                                      settings.FILE_STORAGE_PATH, 
                                      str(project_id))
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        file_path = os.path.join(directory_path, 'lock.json')
        logger.info(f"Saving to {file_path}")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lock, f, ensure_ascii=False)
    except FileNotFoundError:
        logger.warn(f"File not found {file_path}")   
        
def read_lock_file(project_id):
    try:
        directory_path = os.path.join(os.getcwd(), 
                                      settings.FILE_STORAGE_PATH, 
                                      str(project_id))
        file_path = os.path.join(directory_path, 'lock.json')
        f = open(file_path)
        json_data = json.load(f)
        return json_data
    except FileNotFoundError: 
        print("File not found, returning empty")
        return None
    
def delete_lock_file(project_id):
    try:
        directory_path = os.path.join(os.getcwd(), 
                                      settings.FILE_STORAGE_PATH, 
                                      str(project_id))
        file_path = os.path.join(directory_path, 'lock.json')
        os.remove(file_path)
        return True
    except FileNotFoundError:
        logger.warn("Lock not found")
        return True
    except Exception as e:
        logger.error(f"Unable to remove lock project: {project_id}, {e}")
        return False