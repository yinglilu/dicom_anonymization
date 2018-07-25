#!/usr/bin/env python

# anonymize dicom files in input_dir recursively
# follow the BASIC APPLICATION LEVEL CONFIDENTIALITY PROFILE:http://dicom.nema.org/Dicom/supps/sup55_03.pdf
#
# usage: # python dcm_anon.py input_dir

# Author: YingLi Lu
# Date: 2018-07-24
# Ver: 0.1

import os
import argparse
import logging

import pydicom

logging.basicConfig()

# anonymized value
string_anon = 'anon'
date_anon = "18000101"

# modify StudyInstanceUID and SeriesInstanceUID, and keep same StudyInstanceUID/SeriesInstanceUID for each study/series
StudyInstanceUID_dict = {}
SeriesInstanceUID_dict = {}


def anonymize(dicom_file, output_dir):
    ds = pydicom.dcmread(dicom_file, stop_before_pixels=True)

    # modify StudyInstanceUID
    if 'StudyInstanceUID' in ds:
        if ds.StudyInstanceUID in StudyInstanceUID_dict:
            ds.StudyInstanceUID = StudyInstanceUID_dict[ds.StudyInstanceUID]
        else:
            StudyInstanceUID_dict[ds.StudyInstanceUID] = pydicom.uid.generate_uid(
            )
            ds.StudyInstanceUID = StudyInstanceUID_dict[ds.StudyInstanceUID]

    # modify SeriesInstanceUID
    if 'SeriesInstanceUID' in ds:
        if ds.SeriesInstanceUID in SeriesInstanceUID_dict:
            ds.SeriesInstanceUID = SeriesInstanceUID_dict[ds.SeriesInstanceUID]
        else:
            SeriesInstanceUID_dict[ds.SeriesInstanceUID] = pydicom.uid.generate_uid(
            )
            ds.SeriesInstanceUID = SeriesInstanceUID_dict[ds.SeriesInstanceUID]

    # Patient's Name (0010,0010)
    if 'PatientName' in ds:
        ds.PatientName = string_anon

    # # Patient ID (0010,0020)
    if 'PatientID' in ds:
        ds.PatientID = string_anon

    # Patient's Birth Date (0010,0030)
    if 'StudyDate' in ds:
        ds.StudyDate = date_anon

    # Patient's Birth Date (0010,0030)
    if 'PatientBirthDate' in ds:
        ds.PatientBirthDate = date_anon

    # Patient's Sex (0010,0040)
    if 'PatientSex' in ds:
        ds.PatientSex = string_anon

    # Patient's Birth Time (0010,0032)
    if 'PatientBirthTime' in ds:
        ds.PatientBirthTime = string_anon

    # Other Patient IDs (0010,1000)
    if 'OtherPatientIDs' in ds:
        ds.OtherPatientIDs = string_anon

    # Other Patient Names (0010,1001)
    if 'OtherPatientNames' in ds:
        ds.OtherPatientNames = string_anon

    # Ethnic Group (0010,2160)
    if 'EthnicGroup' in ds:
        ds.EthnicGroup = string_anon

    # Patient Comments (0010,4000)
    if 'PatientComments' in ds:
        ds.PatientComments = string_anon

    # Referring Physician's Name (0008,0090)
    if 'ReferringPhysicianName' in ds:
        ds.ReferringPhysicianName = string_anon

    # Study ID (0020,0010)
    if 'StudyID' in ds:
        ds.StudyID = string_anon

    # Accession Number (0008,0050)
    if 'AccessionNumber' in ds:
        ds.AccessionNumber = string_anon

    # # cfmm's sort_rule.py need this tag
    # # Study Description (0008,1030)
    # if 'StudyDescription' in ds:
    #     ds.StudyDescription = string_anon

    # Physician(s) of Record (0008,1048)
    if 'PhysiciansOfRecord' in ds:
        ds.	PhysiciansOfRecord = string_anon

    # Name of Physician(s) Reading Study (0008,1060)
    if 'NameOfPhysiciansReadingStudy' in ds:
        ds.NameOfPhysiciansReadingStudy = string_anon

    # Admitting Diagnoses Description (0008,1080)
    if 'AdmittingDiagnosesDescription' in ds:
        ds.AdmittingDiagnosesDescription = string_anon

    # Patient's Age (0010,1010)
    if 'PatientAge' in ds:
        ds.PatientAge = '0'

    # Patient's Size (0010,1020)
    if 'PatientSize' in ds:
        ds.PatientSize = '0'

    # Patient's Weight (0010,1030)
    if 'PatientWeight' in ds:
        ds.PatientWeight = '0'

    # Occupation (0010,2180)
    if 'Occupation' in ds:
        ds.Occupation = string_anon

    # Additional Patient's History (0010,21B0)
    if 'AdditionalPatientHistory' in ds:
        ds.AdditionalPatientHistory = string_anon

    # Performing Physicians'Name (0008,1050)
    if 'PerformingPhysicianName' in ds:
        ds.PerformingPhysicianName = string_anon

    # Protocol Name (0018,1030)
    if 'ProtocolName' in ds:
        ds.ProtocolName = string_anon

    # Series Description (0008,103E)
    if 'SeriesDescription' in ds:
        ds.SeriesDescription = string_anon

    # Operators' Name (0008,1070)
    if 'OperatorsName' in ds:
        ds.OperatorsName = string_anon

    # Institution Name (0008,0080)
    if 'InstitutionName' in ds:
        ds.InstitutionName = string_anon

    # Institution Address (0008,0081)
    if 'InstitutionAddress' in ds:
        ds.InstitutionAddress = string_anon

    # Station Name (0008,1010)
    if 'StationName' in ds:
        ds.StationName = string_anon

    # Institutional Department Name (0008,1040)
    if 'InstitutionalDepartmentName' in ds:
        ds.InstitutionalDepartmentName = string_anon

    # Device Serial Number (0018,1000)
    if 'DeviceSerialNumber' in ds:
        ds.DeviceSerialNumber = string_anon

    # Derivation Description (0008,2111)
    if 'DerivationDescription' in ds:
        ds.DerivationDescription = string_anon

    # Image Comments (0020,4000)
    if 'ImageComments' in ds:
        ds.ImageComments = string_anon

    if 'InstanceNumber' in ds:
        new_dicom_file = str(ds.InstanceNumber).zfill(4)+'.dcm'
    else:
        new_dicom_file = os.path.basename(dicom_file)

    ds.save_as(os.path.join(output_dir, new_dicom_file))


if __name__ == "__main__":

    # argument
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir', help='dir has dicom files')
    parser.add_argument('output_dir', help='save anonymized dicom files to')
    args = parser.parse_args()

    input_root_dir = os.path.abspath(args.input_dir)
    output_root_dir = os.path.abspath(args.output_dir)

    # walk dicom files
    for root_dir, dirs, filenames in os.walk(input_root_dir):
        for filename in filenames:
            full_filename = os.path.join(root_dir, filename)
            output_dir = os.path.dirname(full_filename).replace(
                input_root_dir, output_root_dir)
            try:

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                # anonymize and write new dicom file
                anonymize(full_filename, output_dir)
            except Exception as e:
                logging.error(e)
